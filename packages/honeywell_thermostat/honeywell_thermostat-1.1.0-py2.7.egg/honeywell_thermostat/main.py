from thermostat import get_logger_name, Honeywell
import argparse
import logging.config


def main():
    parser = argparse.ArgumentParser(description="test stub for thermostat.Honeywell",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--username",
                        required=True,
                        help="username required by Honeywell web site")
    parser.add_argument("--password",
                        required=True,
                        help="password required by Honeywell web site")
    parser.add_argument("--unit-id",
                        required=True,
                        type=int,
                        help="the unit id from the Honeywell web site")
    parser.add_argument("--command",
                        required=True,
                        choices=["system-on", "system-off", "cooler", "warmer"],
                        help="small set of acceptable commands")
    args = parser.parse_args()
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger(get_logger_name())
    logger.debug("starting the test")
    honeywell = Honeywell(args.username, args.password, args.unit_id)
    if args.command == "cooler":
        honeywell.cooler(169538, 5)
    elif args.command == "warmer":
        honeywell.warmer(169538, 5)
    elif args.command == "system-on":
        honeywell.system_on()
    elif args.command == "system-off":
        honeywell.system_off()
    elif args.command == "status":
        honeywell.get_status()

if __name__ == "__main__":
    main()
