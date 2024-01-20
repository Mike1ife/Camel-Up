from PIL import Image
from requests import get
from random import choice
from gspread import authorize
from google.oauth2.service_account import Credentials


class Camels:
    def __init__(self):
        self.board = self._start_board()
        self.grid = {
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

        self.red = {"color": "Red", "place": 0, "up": None, "down": None}
        self.blue = {"color": "Blue", "place": 0, "up": None, "down": None}
        self.yellow = {"color": "Yellow", "place": 0, "up": None, "down": None}
        self.purple = {"color": "Purple", "place": 0, "up": None, "down": None}
        self.green = {"color": "Green", "place": 0, "up": None, "down": None}
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

    def _start_board(self):
        board_img = Image.open(
            get(
                "https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/Board.png",
                stream=True,
            ).raw
        ).convert("RGBA")
        return board_img


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


def roll_dice(rows, username, camels):
    rows = add_money(rows, username, 1)

    color = choice(camels.can_move)
    camels.can_move.remove(color)
    step = choice(["1", "2", "3"])
    board = draw_board(color, step, camels)
    return rows, color, step, board


def draw_board(color, step, camels):
    # Get current moving camel
    moving = camels.color2camel[color]
    start = moving["place"]

    # Get the destination
    destination = start + step

    # Get rid of its children
    if moving["down"] != None:
        # Modify true value
        camels.color2camel[color]["down"]["up"] = None
        camels.color2camel[color]["down"] = None
    else:
        # Get rid of the grid if no children
        camels.grid[start] = None

    # Get to destination
    camels.color2camel[color]["place"] = destination
    camels.grid[destination] = camels.color2camel[color]

    total_num = 1
    # Update the infomation of its parents
    unit = f"{color}_"
    next = camels.color2camel[color]["up"]
    while next != None:
        total_num += 1
        unit += f"{next['color']}_"
        # Update the place of its parents
        camels.color2camel[next["color"]]["place"] = destination
        next = camels.color2camel[next["color"]]["up"]

    camel_url = f"https://raw.githubusercontent.com/Mike1ife/Camel-Up/main/images/{unit[:-1]}.png"
    camel_unit_img = Image.open(
        get(
            camel_url,
            stream=True,
        ).raw
    )

    # Draw the result
    board_img = camels.board
    x, y = camels.coordinates[destination][total_num]
    if destination in camels.need_trans:
        camel_unit_img = camel_unit_img.transpose(Image.FLIP_LEFT_RIGHT)

    board_img.paste(camel_unit_img, [x, y], mask=camel_unit_img)
    board_img.show()
    camels.board = board_img

    return board_img


def update_sheet(header, rows, worksheet):
    modified_data = [header] + rows
    worksheet.clear()
    worksheet.update("A1", modified_data)


header, rows, worksheet = init()
camels = Camels()

camels.red["up"] = camels.blue
camels.blue["down"] = camels.red

x = draw_board("Red", 3, camels)
x = draw_board("Blue", 3, camels)


# rows, color, step, board = roll_dice(rows, "Mike", camels)
# update_sheet(header, rows, worksheet)
