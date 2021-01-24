# Link3 CLI

CLI for [Link3 Selfcare](https://selfcare.link3.net/)

## Installation

```bash
sudo pip3 install click tabulate
sudo install -m 775 link3.py /usr/local/bin/link3 # or anything you prefer
```

## How to Use

```
Usage: link3 [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  account   Show account information
  login     Login to portal
  payments  Show online payment history
  tickets   Show ticket history
```

### Login

```
~ $ link3 login -u L3R12345678 -p PSWD!@#$
Login success. Please export L3_PHPSESSID=dupfm56clhflm49nv01u8ndlib
```

Then export it.

```bash
export L3_PHPSESSID=dupfm56clhflm49nv01u8ndlib
```

### View Account Information

```
~ $ link3 account
----------------------------   ---------------------
Subscriber ID                  L3R12345678
Package Name                   Falcon Plus Up Booster
Status Falcon Plus Up Booster  Active
Expire Date                    2021-12-31
Balance                        2789 Taka
----------------------------   ---------------------
```

### View Payment History

```
~ $ link3 payments
date        gateway    amount    invoice
----------  ---------  --------  ----------------------------------------------------------------
01-01-2021  CityBank   2789 BDT  https://selfcare.link3.net/DownloadReceipt/TM3NSMMTE0TD/DQNTzOk=
01-12-2020  CityBank   2789 BDT  https://selfcare.link3.net/DownloadReceipt/TM3NSMMTE0TD/MzNDA1I=
```

### View Ticket History

```
~ $ link3 tickets
date                   ticket  category     status    action
-------------------  --------  -----------  --------  ----------------------------------------------------
2021-01-03 15:43:08    788198  LAN Problem  Resolved  https://selfcare.link3.net/ticketdetails/?TID=788198
```
