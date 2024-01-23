from PIL import Image
from requests import get
from random import choice
from gspread import authorize
from google.oauth2.service_account import Credentials


class Game:
    grid = {
        1: None,
        2: None,
        3: None,
        4: None,
        5: None,
        6: None,
        7: None,
        8: None,
        9: None,
        10: None,
        11: None,
        12: None,
        13: None,
        14: None,
        15: None,
        16: None,
    }

    traps = {
        1: None,
        2: None,
        3: None,
        4: None,
        5: None,
        6: None,
        7: None,
        8: None,
        9: None,
        10: None,
        11: None,
        12: None,
        13: None,
        14: None,
        15: None,
        16: None,
    }

    def __init__(self):
        self.board = Image.open(
            get(
                "https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/Board.png",
                stream=True,
            ).raw
        ).convert("RGBA")

        self.red = Camel("Red")
        self.blue = Camel("Blue")
        self.yellow = Camel("Yellow")
        self.purple = Camel("Purple")
        self.green = Camel("Green")

        self.color2camel = {
            "Red": self.red,
            "Blue": self.blue,
            "Yellow": self.yellow,
            "Purple": self.purple,
            "Green": self.green,
        }
        self.can_move = ["Red", "Blue", "Yellow", "Purple", "Green"]

        self.need_trans = [1, 2, 3, 4, 13, 14, 15, 16]
        self.coordinates = {
            1: {
                1: (980, 1390),
                2: (980, 1335),
                3: (980, 1280),
                4: (980, 1225),
                5: (980, 1170),
            },
            2: {
                1: (680, 1390),
                2: (680, 1335),
                3: (680, 1280),
                4: (680, 1225),
                5: (680, 1170),
            },
            3: {
                1: (380, 1390),
                2: (380, 1335),
                3: (380, 1280),
                4: (380, 1225),
                5: (380, 1170),
            },
            4: {
                1: (80, 1390),
                2: (80, 1335),
                3: (80, 1280),
                4: (80, 1225),
                5: (80, 1170),
            },
            5: {1: (80, 1090), 2: (80, 1035), 3: (80, 980), 4: (80, 925), 5: (80, 870)},
            6: {1: (80, 790), 2: (80, 735), 3: (80, 680), 4: (80, 625), 5: (80, 570)},
            7: {1: (80, 490), 2: (80, 435), 3: (80, 380), 4: (80, 325), 5: (80, 270)},
            8: {1: (80, 190), 2: (80, 135), 3: (80, 80), 4: (80, 25), 5: (80, -30)},
            9: {
                1: (380, 200),
                2: (380, 145),
                3: (380, 90),
                4: (380, 35),
                5: (380, -20),
            },
            10: {
                1: (680, 200),
                2: (680, 145),
                3: (680, 90),
                4: (680, 35),
                5: (680, -20),
            },
            11: {
                1: (980, 200),
                2: (980, 145),
                3: (980, 90),
                4: (980, 35),
                5: (980, -20),
            },
            12: {
                1: (1280, 200),
                2: (1280, 145),
                3: (1280, 90),
                4: (1280, 35),
                5: (1280, -20),
            },
            13: {
                1: (1280, 500),
                2: (1280, 445),
                3: (1280, 390),
                4: (1280, 335),
                5: (1280, 280),
            },
            14: {
                1: (1280, 800),
                2: (1280, 745),
                3: (1280, 690),
                4: (1280, 635),
                5: (1280, 580),
            },
            15: {
                1: (1280, 1100),
                2: (1280, 1045),
                3: (1280, 990),
                4: (1280, 935),
                5: (1280, 880),
            },
            16: {
                1: (1280, 1400),
                2: (1280, 1345),
                3: (1280, 1290),
                4: (1280, 1235),
                5: (1280, 1180),
            },
        }

    def restart_round(self):
        self.can_move = ["Red", "Blue", "Yellow", "Purple", "Green"]
        self.traps = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
        }

    def roll_dice(self, rows, username):
        rows = add_money(rows, username, 1)

        color = choice(self.can_move)
        self.can_move.remove(color)
        step = choice([1, 2, 3])
        is_over, winner = self.color2camel[color].move_forward(step)
        board_image = self.draw_board()
        return (rows, color, step, board_image, is_over, winner)

    def draw_board(self):
        # Draw the result
        board_img = self.board.copy()
        for place, camel in self.grid.items():
            if camel != None:
                total_num = 1
                # The color of current camel
                color = camel.color
                # The color of this unit
                unit = f"{color}_"
                next = self.color2camel[color].up
                while next != None:
                    total_num += 1
                    unit += f"{next.color}_"
                    next = next.up

                camel_url = f"https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/{unit[:-1]}.png"

                camel_unit_img = Image.open(
                    get(
                        camel_url,
                        stream=True,
                    ).raw
                )

                x, y = self.coordinates[place][total_num]
                if place in self.need_trans:
                    camel_unit_img = camel_unit_img.transpose(Image.FLIP_LEFT_RIGHT)

                board_img.paste(camel_unit_img, [x, y], mask=camel_unit_img)

        for place, trap in self.traps.items():
            if trap != None:
                trap_card = Image.open(f"images/Trap_{trap.method}.png").convert("RGBA")
                x, y = self.coordinates[place][3]

                board_img.paste(trap_card, box=[x - 50, y - 30], mask=trap_card)

        return board_img

    def _get_coordinate(self):
        # [pos, number]
        coordinates = {}
        """Bot Line: 1 2 3 4"""
        for i in range(1, 5):
            coordinate = {}
            x = 1280 - 300 * i
            for num_cam in range(0, 5):
                y = 1390 - 55 * num_cam
                coordinate[num_cam + 1] = (x, y)
            coordinates[i] = coordinate

        """Left Line: 5 6 7 8"""
        for i in range(5, 9):
            coordinate = {}
            x = 80
            for num_cam in range(0, 5):
                y = 1390 - 300 * (i - 4) - 55 * num_cam
                coordinate[num_cam + 1] = (x, y)
            coordinates[i] = coordinate

        """Top Line: 9 10 11 12"""
        for i in range(9, 13):
            coordinate = {}
            x = 80 + 300 * (i - 8)
            for num_cam in range(0, 5):
                y = 200 - 55 * num_cam
                coordinate[num_cam + 1] = (x, y)
            coordinates[i] = coordinate

        """Right Line: 13 14 15 16"""
        for i in range(13, 17):
            coordinate = {}
            x = 1280
            for num_cam in range(0, 5):
                y = 200 + 300 * (i - 12) - 55 * num_cam
                coordinate[num_cam + 1] = (x, y)
            coordinates[i] = coordinate
        return coordinates

    def get_grid_info(self, place):
        return self.grid[place]

    def update_grid_info(self, place, camel):
        self.grid[place] = camel

    def place_trap(self, place, method):
        new_trap = Trap("Mike", place, method)
        self.traps[place] = new_trap

    def get_trap_info(self, place):
        return self.traps[place]


class Camel(Game):
    def __init__(self, color):
        self.color = color
        self.place = 0
        self.up = None
        self.down = None

    def move_forward(self, step):
        print(f"{self.color} 往前走 {step} 步")

        is_over, winner = False, None
        # Get current moving camel
        start = self.place

        # Get the destination
        destination = start + step

        if destination > 16:
            is_over = True
            destination %= 16
            winner = self
            while winner.up != None:
                winner = winner.up

        # Get rid of its children
        if self.down != None:
            # Modify true value
            self.down.up = None
            self.down = None
        else:
            # Get rid of the grid if no children
            self.update_grid_info(start, None)

        # Get to destination
        self.place = destination
        if self.get_grid_info(destination) == None:
            # If no other camel in destination
            self.update_grid_info(destination, self)
        else:
            # Go up to the camel
            next = self.get_grid_info(destination)
            while next.up != None:
                next = next.up

            next.up = self
            self.down = next

        # Update the infomation of its parents
        next = self.up
        while next != None:
            # Update the place of its parents
            next.place = destination
            next = next.up

        # Step on a Trap
        if self.get_trap_info(destination) != None:
            print(f"{self.color} 踩到 {self.get_trap_info(destination).method}")
            if self.get_trap_info(destination).method == "Add":
                is_over, winner = self.move_forward(1)
            elif self.get_trap_info(destination).method == "Minus":
                self.move_backward(1)

        return is_over, winner

    def move_backward(self, step):
        print(f"{self.color} 往後走 {step} 步")

        # Get current moving camel
        start = self.place

        # Get the destination
        destination = start - step

        # Get rid of the grid (Trap -> No children)
        self.update_grid_info(start, None)

        # Get to destination
        self.place = destination
        if self.get_grid_info(destination) != None:
            # Go down to the camel
            unit_top = self
            # Get the camel on the top
            while unit_top.up != None:
                unit_top = unit_top.up
            # Go down to the existing camel
            self.get_grid_info(destination).down = unit_top
            unit_top.up = self.get_grid_info(destination)

        # Update grid infomation
        self.update_grid_info(destination, self)

        # Update the infomation of its parents
        next = self.up
        while next != None:
            # Update the place of its parents
            next.place = destination
            next = next.up


class Trap:
    def __init__(self, username, place, method):
        self.username = username
        self.place = place
        self.method = method


def init():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("game_table.json", scopes=scope)
    gs = authorize(creds)

    sheet = gs.open_by_url(
        "https://docs.google.com/spreadsheets/d/1F_kneSkIuasryz6XMHgaAUvEejVO_Xn-b4lO5xQ5Occ/edit#gid=0"
    )
    worksheet = sheet.get_worksheet(0)
    data = worksheet.get_all_values()

    header, rows = data[0], data[1:]
    return header, rows, worksheet


def add_money(rows, username, value):
    for row in rows:
        if row[0] == username:
            row[1] = int(row[1]) + value
            return rows


def update_sheet(header, rows, worksheet):
    modified_data = [header] + rows
    worksheet.clear()
    worksheet.update("A1", modified_data)


header, rows, worksheet = init()
game = Game()
game.place_trap(2, "Minus")

while True:
    game_over = False
    for j in range(5):
        if len(game.can_move) == 0:
            game.restart_round()
        rows, color, step, board_image, is_over, winner = game.roll_dice(rows, "Mike")
        board_image.show()
        if is_over:
            game_over = True
            print(f"{winner.color} 獲勝！")
            break
    if game_over:
        break


# update_sheet(header, rows, worksheet)
