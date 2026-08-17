if __name__ == "__main__":
    from config import config
    from ok import OK

    config = config
    config["gui"] = {
        "type": "web",
        "launch_mode": "pywebview",  # default
    }
    ok = OK(config)
    ok.start()
