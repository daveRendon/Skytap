# Performance Navigator AIX

### Option 1 - Install Performance Navigator to begin collecting historical NMON data.

> **Note:** The host code data collection is free, has no CPU overhead, and requires less than 5GB of disk space even after several years.

1. On AIX / Linux, run as `root`. In the case of VIOS, you need to login as `padmin` and then type `oem_setup_env`.
2. Download `powernav.tar.gz` from [https://cdn.fortra.com/software/robot/performance-nav/powernav.tar.gz](https://cdn.fortra.com/software/robot/performance-nav/powernav.tar.gz).
3. FTP to `/tmp` [or any other directory, just note that the next step refers to `/tmp`].
4. If the system already has NMON running and/or there is a central repository, go to the next section to use the existing data.
5. Run the following command:

    ```bash
    cd /tmp; gunzip -f powernav.tar.gz; tar -xvf powernav.tar; ./install.sh
    ```

    > **Note:** The install stores data in `/usr/local/mpg` and is scheduled via cron entries.

6. After 7 or more days, send us the file in `/usr/local/mpg` called `pninfo_hostname.tar.gz`.

### Option 2 - Use existing NMON data.

If the system already has historical NMON data, we can use the existing NMON data.

1. Download `pnbuild.tar.gz` from [https://cdn.fortra.com/software/robot/performance-nav/pnbuild.tar.gz](https://cdn.fortra.com/software/robot/performance-nav/pnbuild.tar.gz).
2. FTP `pnbuild.tar.gz` to the same directory as the existing NMON directory. This directory can have NMON data from multiple partitions or even subdirectories for each partition.
3. Unzip, untar all files, and run the script:

    ```bash
    ./pnbmpgd2gzip.sh
    ```

    > **Note:** To save space, this script will GZ existing NMON files. If already GZed, we will process them as well. Ensure the file system has enough space to basically double the data (if already GZed).

### Sending AIX/Linux/VIOS Data

The script will create a file called `pninfo_hostname` or `multiple.tar.gz`. Send those files.

### Option 3 - Topas Data

By default, AIX systems have 7 days of Topas data. This data is good enough for CPU core capacity planning but lacks detailed data for disk and memory. This is most often used for VIOS partitions.

1. Download the Topas data script from [https://cdn.fortra.com/software/robot/performance-nav/pnbuild.tar.gz](https://cdn.fortra.com/software/robot/performance-nav/pnbuild.tar.gz).
2. FTP `pnbuild.tar.gz` to `/tmp`, unzip, untar, and run:

    ```bash
    ./rackdata.sh -T
    ```

3. This will create a file called `pninfo_topas_hostname_datetime.tar.gz`. Just send this file.
