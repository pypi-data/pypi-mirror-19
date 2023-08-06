from melee import enums, characterstats
import csv
from struct import *
import binascii
import os
import socket

"""Represents the state of a running game of Melee at a given moment in time"""
class GameState:
    frame = 0
    stage = enums.Stage.FINAL_DESTINATION
    menu_state = enums.Menu.CHARACTER_SELECT
    player = dict()
    projectiles = []
    stage_select_cursor_x = 0.0
    stage_select_cursor_y = 0.0
    ready_to_start = False

    def __init__(self, dolphin):
        #Dict with key of address, and value of (name, player)
        self.locations = dict()
        #Copy the locations.csv adjacent to this file
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + "/locations.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                self.locations[line["Address"]] = (line["Name"], line["Player"])
        self.player[1] = PlayerState()
        self.player[2] = PlayerState()
        self.player[3] = PlayerState()
        self.player[4] = PlayerState()
        self.newframe = True
        #Helper names to keep track of us and our opponent
        self.ai_state = self.player[dolphin.ai_port]
        self.opponent_state = self.player[dolphin.opponent_port]

        #Creates the socket if it does not exist, and then opens it.
        path = dolphin.get_memory_watcher_socket_path()
        try:
            os.unlink(path)
        except OSError:
            pass
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.sock.bind(path)

    """Return a list representation of the current gamestate
    Only caring about in-game things, not menus and such"""
    def tolist(self):
        thelist = []
        thelist.append(self.frame)
        thelist.append(self.stage.value)
        thelist = thelist + self.ai_state.tolist()
        thelist = thelist + self.opponent_state.tolist()
        #TODO: Figure out the best way to add projectiles to the list
        #thelist = thelist + self.projectiles.tolist()
        return thelist

    """Process one new memory update
       returns True if the frame is finished processing (no more updates this frame)
       Run this in a loop until it returns returns True, then press your buttons,
       wash, rinse, repeat."""
    def update(self, mem_update):
        label = self.locations[mem_update[0]][0]
        player_int = int(self.locations[mem_update[0]][1])
        if label == "frame":
            self.frame = unpack('<I', mem_update[1])[0]
            self.newframe = True
            return True
        if label == "stage":
            self.stage = unpack('<I', mem_update[1])[0]
            self.stage = self.stage >> 16
            try:
                self.stage = enums.Stage(self.stage)
            except ValueError:
                self.stage = enums.Stage.NO_STAGE
            return False
        if label == "menu_state":
            self.menu_state = unpack('<I', mem_update[1])[0]
            self.menu_state &= 0x000000ff
            self.menu_state = enums.Menu(self.menu_state)
            return False
        #Player variables
        if label == "percent":
            self.player[player_int].percent = unpack('<I', mem_update[1])[0]
            self.player[player_int].percent = self.player[player_int].percent >> 16
            return False
        if label == "stock":
            self.player[player_int].stock = unpack('<I', mem_update[1])[0]
            self.player[player_int].stock = self.player[player_int].stock >> 24
            return False
        if label == "facing":
            self.player[player_int].facing = unpack('<I', mem_update[1])[0]
            self.player[player_int].facing = self.player[player_int].facing >> 31
            return False
        if label == "x":
            self.player[player_int].x = unpack('<f', mem_update[1])[0]
            return False
        if label == "y":
            self.player[player_int].y = unpack('<f', mem_update[1])[0]
            return False
        if label == "character":
            temp = unpack('<I', mem_update[1])[0] >> 24
            try:
                self.player[player_int].character = enums.Character(temp)
            except ValueError:
                self.player[player_int].character = enums.Character.UNKNOWN_CHARACTER
            return False
        if label == "cursor_x":
            self.player[player_int].cursor_x = unpack('<f', mem_update[1])[0]
            return False
        if label == "cursor_y":
            self.player[player_int].cursor_y = unpack('<f', mem_update[1])[0]
            return False
        if label == "action":
            temp = unpack('<I', mem_update[1])[0]
            try:
                self.player[player_int].action = enums.Action(temp)
            except ValueError:
                self.player[player_int].action = enums.Action.UNKNOWN_ANIMATION
            return False
        if label == "action_counter":
            #TODO look if this is backwards
            temp = unpack('I', mem_update[1])[0]
            temp = temp >> 8
            self.player[player_int].action_counter = temp
            return False
        if label == "action_frame":
            temp = unpack('<f', mem_update[1])[0]
            try:
                self.player[player_int].action_frame = int(temp)
            except ValueError:
                pass
            return False
        if label == "invulnerable":
            self.player[player_int].invulnerable = unpack('<I', mem_update[1])[0]
            self.player[player_int].invulnerable = self.player[player_int].invulnerable >> 31
            return False
        if label == "hitlag_frames_left":
            temp = unpack('<f', mem_update[1])[0]
            try:
                self.player[player_int].hitlag_frames_left = int(temp)
            except ValueError:
                pass
            return False
        if label == "hitstun_frames_left":
            temp = unpack('<f', mem_update[1])[0]
            try:
                self.player[player_int].hitstun_frames_left = int(temp)
            except ValueError:
                pass
            return False
        if label == "charging_smash":
            temp = unpack('<I', mem_update[1])[0]
            if temp == 2:
                self.player[player_int].charging_smash = True
            else:
                self.player[player_int].charging_smash = False
            return False
        if label == "jumps_left":
            temp = unpack('<I', mem_update[1])[0]
            temp = temp >> 24
            #This value is actually the number of jumps USED
            #   so we have to do some quick math to turn this into what we want
            temp = characterstats.maxjumps(self.player[player_int].character) - temp + 1
            self.player[player_int].jumps_left = temp
            return False
        if label == "on_ground":
            temp = unpack('<I', mem_update[1])[0]
            if temp == 0:
                self.player[player_int].on_ground = True
            else:
                self.player[player_int].on_ground = False
            return False
        if label == "speed_air_x_self":
            self.player[player_int].speed_air_x_self = unpack('<f', mem_update[1])[0]
            return False
        if label == "speed_y_self":
            self.player[player_int].speed_y_self = unpack('<f', mem_update[1])[0]
            return False
        if label == "speed_x_attack":
            self.player[player_int].speed_x_attack = unpack('<f', mem_update[1])[0]
            return False
        if label == "speed_y_attack":
            self.player[player_int].speed_y_attack = unpack('<f', mem_update[1])[0]
            return False
        if label == "speed_ground_x_self":
            self.player[player_int].speed_ground_x_self = unpack('<f', mem_update[1])[0]
            return False
        if label == "coin_down":
            temp = unpack('<I', mem_update[1])[0]
            temp = temp & 0x000000ff
            self.player[player_int].coin_down = (temp == 2)
        if label == "stage_select_cursor_x":
            self.stage_select_cursor_x = unpack('<f', mem_update[1])[0]
            return False
        if label == "stage_select_cursor_y":
            self.stage_select_cursor_y = unpack('<f', mem_update[1])[0]
            return False
        if label == "ready_to_start":
            temp = unpack('>I', mem_update[1])[0]
            temp = temp & 0x000000ff
            self.ready_to_start = bool(temp)
        if label == "projectiles":
            #Only once per new frame that we get a projectile, clear the list out
            if self.newframe:
                self.projectiles.clear()
                self.i = 0
            self.i += 1
            self.newframe = False
            if len(mem_update[1]) < 10:
                self.projectiles.clear()
                return False
            proj = Projectile()
            proj.x = unpack('>f', mem_update[1][0x4c:0x50])[0]
            proj.y = unpack('>f', mem_update[1][0x50:0x54])[0]
            proj.x_speed = unpack('>f', mem_update[1][0x40:0x44])[0]
            proj.y_speed = unpack('>f', mem_update[1][0x44:0x48])[0]
            try:
                proj.subtype = enums.ProjectileSubtype(unpack('>I', mem_update[1][0x10:0x14])[0])
            except ValueError:
                proj.subtype = enums.ProjectileSubtype.UNKNOWN_PROJECTILE
            self.projectiles.append(proj)
        return False

    """Iterate over this class in the usual way to get memory changes."""
    def __iter__(self):
        return self

    """Closes the socket."""
    def __del__(self):
        self.sock.close()

    """Returns the next (address, value) tuple, or None on timeout.
    address is the string provided by dolphin, set in Locations.txt.
    value is a four-byte string suitable for interpretation with struct.
    """
    def __next__(self):
        try:
            data = self.sock.recvfrom(9096)[0].decode('utf-8').splitlines()
        except socket.timeout:
            return None
        # Strip the null terminator, pad with zeros, then convert to bytes
        return data[0], binascii.unhexlify(data[1].strip('\x00').zfill(8))

"""Represents the state of a single player"""
class PlayerState:
    character = enums.Character.UNKNOWN_CHARACTER
    x = 0
    y = 0
    percent = 0
    stock = 0
    facing = True
    action = enums.Action.UNKNOWN_ANIMATION
    action_counter = 0
    action_frame = 0
    invulnerable = False
    hitlag_frames_left = 0
    hitstun_frames_left = 0
    charging_smash = 0
    jumps_left = 0
    on_ground = True
    speed_air_x_self = 0
    speed_y_self = 0
    speed_x_attack = 0
    speed_y_attack = 0
    speed_ground_x_self = 0
    cursor_x = 0
    cursor_y = 0
    coin_down = False

    """Produces a list representation of the player's state"""
    def tolist(self):
        thelist = []
        thelist.append(self.x)
        thelist.append(self.y)
        thelist.append(self.percent)
        thelist.append(self.stock)
        thelist.append(int(self.facing))
        thelist.append(self.action.value)
        #We're... gonna leave this one out for now since it's a bit irrelevant
        #thelist.append(self.action_counter)
        thelist.append(self.action_frame)
        thelist.append(int(self.invulnerable))
        thelist.append(self.hitlag_frames_left)
        thelist.append(self.hitstun_frames_left)
        thelist.append(int(self.charging_smash))
        thelist.append(self.jumps_left)
        thelist.append(int(self.on_ground))
        #We're combining speeds here for simplicity's sake
        thelist.append(self.speed_air_x_self + self.speed_x_attack + self.speed_ground_x_self)
        thelist.append(self.speed_y_self + self.speed_y_attack)
        return thelist

"""Represents the state of a projectile (items, lasers, etc...)"""
class Projectile:
    x = 0
    y = 0
    x_speed = 0
    y_speed = 0
    opponent_owned = True
    subtype = enums.ProjectileSubtype.UNKNOWN_PROJECTILE

    """Produces a list representation of the projectile"""
    def tolist(self):
        thelist = []
        thelist.append(self.x)
        thelist.append(self.y)
        thelist.append(self.x_speed)
        thelist.append(self.y_speed)
        thelist.append(int(self.opponent_owned))
        thelist.append(self.subtype.value)
        return thelist
