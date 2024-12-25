# Netcup Traffic Reset

[中文版本](README.md) | English Version

## Netcup Traffic Reset

This project is a tool for automatically managing **Netcup vServer** and **qBittorrent** download tasks. By calling the Netcup API and qBittorrent API, it automates server restarts and the pausing/resuming of torrent tasks.

---

## Environment Variable Configuration

Before running the project, please configure the environment variables as follows:

1. Copy the `env.example` file to `.env`:

    ```bash
    cp .env.example .env
    ```

2. Edit the `.env` file according to your needs and fill in the correct configuration information:

    ```plaintext
    # Netcup Customer ID
    NETCUP_CUSTOMER_ID=your_customer_id
    # The Netcup Web API password is not your login password.
    # This password can be found in the "Options" menu in the top right corner of the Netcup SCP backend, specifically in the "Webservice" section under "Webservice Password".
    # Please also ensure that the "Activate Webservice" function is enabled and save the settings.
    NETCUP_API_PASSWORD=your_api_password
    # Netcup VServer ID, also found in the "Server" list in the SCP console
    DEFAULT_VSERVER=your_default_vserver
    # qBittorrent Web API address
    QB_API_URL=http://127.0.0.1:8080
    # qBittorrent login username
    QB_USERNAME=admin
    # qBittorrent login password
    QB_PASSWORD=admin
    # Define the daily task time (24-hour format, format: HH:MM)
    DAILY_TASK_TIME=04:00
    ```

---

## Docker Deployment

### Git Clone Repository for Self-Building

1. **Build the Image**

    First, clone this project repository to your local machine:

    ```bash
    git clone https://github.com/kafuuchino-s/netcup-traffic-reset
    cd netcup-traffic-reset
    ```

    Then, use the following command to build the Docker image:

    ```bash
    docker build -t netcup-traffic-reset:latest .
    ```

2. **Run the Container**

    After building, use the following command to run the container and mount the `.env` configuration file:

    ```bash
    docker run --rm -d \
      --env-file .env \
      --name netcup-traffic-reset \
      netcup-traffic-reset:latest
    ```

### Directly Launch Using the kafuuchino520/netcup-traffic-reset Image

You can directly use the pre-built image provided on Docker Hub to run:

```bash
docker run --rm -d \
  --env-file .env \
  --name netcup-traffic-reset \
  kafuuchino520/netcup-traffic-reset:latest
```

---

## Functionality Description

1. **Automated Reset Process**
    -   Pause qBittorrent torrent tasks.
    -   Restart the Netcup vServer (via Power Cycle or ACPI restart).
    -   After checking that the network status has recovered, restart the torrent tasks.
2. **Scheduled Task Support**
    -   Set the scheduled task time through `DAILY_TASK_TIME` in the `.env` file, defaulting to 4 AM daily.
3. **Lightweight Deployment**
    -   Quick deployment using the official Docker image, without the need to install complex dependencies.

---

## Common Issues

1. **Unable to connect to the qBittorrent API?**
    -   Check if `QB_API_URL` in the `.env` file is filled in correctly.
    -   Ensure that the qBittorrent Web API is enabled and that the correct username and password are set.
2. **Netcup API call failed?**
    -   Check if `NETCUP_CUSTOMER_ID` and `NETCUP_API_PASSWORD` in the `.env` file are correct.
    -   Ensure that you have enabled the "Activate Webservice" function in the Netcup SCP backend and are using the correct Webservice password.
3. **Scheduled task not taking effect?**
    -   Ensure that the `DAILY_TASK_TIME` format in the `.env` file is correct.
    -   If you have modified `.env`, please restart the container.

---

## Summary

-   **Simple Configuration**: Manage all configuration items centrally through the `.env` file.
-   **Convenient Deployment**: Use the official Docker image without the need for additional building.
-   **Automated Process**: Supports scheduled tasks, making it easy to implement server traffic reset and torrent task management.

## Project References

-   [mihneamanolache/netcup-webservice](https://github.com/mihneamanolache/netcup-webservice)
-   [qbittorrent-api](https://pypi.org/project/qbittorrent-api/)

If you have any questions or suggestions, please submit an Issue!
