# floor-board

A data visualization program that allows McDonald's teams to visualize product sales data in real-time. 

> **floor-board can request XML receipt data from a McDonald's NP6 server and display relevant information using [Eel](https://github.com/ChrisKnott/Eel).**

floor-board can connect to the [dotops API](https://github.com/isaiah-gordon/dotops) to share sales data between stores and make suggestive selling competitive.


<p align="center"><img src="https://storage.googleapis.com/dotops.app/floor_board_image.jpg" ></p>


- [floor-board](#floor-board)
  - [Setup](#setup)
    - [Install](#install)
    - [Configure](#configure)


## Setup
floor-board has been tested and designed to run on [Ubuntu Desktop](https://ubuntu.com/download/desktop) 20.04.2.0 LTS.

### Install
- Install the latest version of Chrome [here](https://www.google.com/intl/en_ca/chrome/).

**Run the following commands in the Ubuntu Desktop terminal:**

- Reinstall the emoji font pack `sudo apt reinstall fonts-noto-color-emoji`

- Clone the floor-board repository `sudo git clone https://github.com/isaiah-gordon/floor-board.git`

- Move to the floor-board directory `cd floor-board`

- Install floor-board dependencies `pip3 install -r requirements.txt`

### Configure
floor-board requires a `config.json` file in order to run.

**Example of config.json:**
```
{
  "store_number": "12134",
  "lane_type": "dual",
  "idle_type": "covid_safety",
  "rmu_address": "192.0.123.456",
  "rmu_username": "123",
  "rmu_password": "456",
  "dotops_token": "DOTOPS_WEBTOKEN"
}
```

**Key definitions for config.json:**

`store_number` The national store number of the store floor-board is being setup in.

`lane_type` The drive thru type of the store floor-board is being setup in (either "single" or "dual").

`idle_type` Content to be displayed while floor-board is idle (either "covid_safety" or "").

`rmu_address` The URL for the RMU in the store floor-board is being setup in.

`rmu_username` An authorized manager ID in the store floor-board is being setup in.

`rmu_password` The code corresponding to the manager ID in "rmu_username".

`dotops_token` A unique JSON web token for the dotops API.
