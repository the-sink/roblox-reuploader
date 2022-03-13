<img src="resources/icon.png" align="right" height="84" />

# Roblox Bulk Reupload Tool [![License](https://img.shields.io/github/license/the-sink/roblox-reuploader)](https://github.com/the-sink/roblox-reuploader/blob/main/LICENSE) [![Issues](https://img.shields.io/github/issues/the-sink/roblox-reuploader)](https://github.com/the-sink/roblox-reuploader/issues)

As many are already well aware of, [Roblox is making it so that audio above 6 seconds can only be used if you are the uploader](https://devforum.roblox.com/t/action-needed-upcoming-changes-to-asset-privacy-for-audio/1701697) on March 22nd 2022. This tool's objective is to ease the process of transitioning your game over, by automatically collecting all audio that requires migration and automatically re-uploading it into your profile (or the group, if you're running this in a group game).

# Warnings
**THIS TOOL IS EXPERIMENTAL!** I developed it fairly quickly and have not had ample opportunities yet to thoroughly test it. If you are migrating a game with a lot of audio assets, please closely monitor the profile that audio is being uploaded to and ensure nothing is going wrong. If you notice any unusual errors or behavior, feel free to contact me or submit an issue.

**Make sure you have the quota available to upload all of the audio.** Another change as a result of this is that audio uploads are now free - but every user has a monthly quota that is dependent on a few factors (such as whether you are ID verified). You can check your quota by visiting the audio upload page on the website. The plugin will display the **maximum** total number of assets it intends to upload on-screen and will require you to confirm this. Keep in mind, this number is not *neccesarily* the final amount of assets that will be uploaded, as it keeps a running list of all of the assets it has previously uploaded (these are used instead of uploading duplicates). Invalid/copyrighted assets and HTTP errors can affect this as well, of course.

# How to use

Keep in mind, this tool has only been tested on Windows 10 so far.

## Step 0: Download Python (if you don't have it already)

The first step is to make sure you have Python. The reupload server is written in Python and will be required at all times.

You can download Python [here](https://www.python.org/). The version I have personally tested this on is **3.10.2**.

If you are installing it for the first time, it is likely you will need to restart (or sign out and sign back in), so do that once you have.

## Step 1: Download server & plugin

Locate the "Download ZIP" button and download this repo to your machine:

![Step1](https://i.imgur.com/OW7CcFW.png)

Unzip the contents into a folder somewhere **safe** (there is a file the server will create that you wlll not want to lose).

Open a command line window in the same folder as the repo's files. One quick way to do this is by clicking on the address bar in explorer and entering `cmd`.

![cmd](https://i.imgur.com/6kH0XII.png)

Once a command window is open in this location, install the neccesary dependencies with `pip install -Ur requirements.txt`.

If no fatal errors occur, you are ready to proceed.

## Step 2: Obtain Roblox cookies

This tool requires your .ROBLOSECURITY and .RBXID cookies to function, due to a fairly restrictive toolbox API endpoint that is used for bulk asset information.

Normally, it is **not** a good idea to share these, but this tool will not do anything malicious with your cookies and is required for it to function.

These cookies can be located on your browser while the Roblox website is open. You can look up a guide on how to do this for your specific browser, but for Chrome it involves:

* Opening the developer tools (Ctrl+Shift+I)
* Navigating to the "Application" tab
* Clicking on the "Cookies" category on the sidebar
* Clicking on the Roblox URL inside this dropdown
* Locating the neccesary cookies in the list

The "Value" field of these cookies must be copied, in full, to a config file. Create a copy of the `config.example.py` file and rename it to just `config.py`.

In the config file, place the `.ROBLOSECURITY` and `.RBXID` cookies into the quotes on the corresponding lines.

Once the cookies are added, you should be ready on the server side.

## Step 3: Install Roblox plugin

A copy of the required plugin exists in the repo: `AudioUpload.rbxmx` (it will be uploaded to Roblox once the plugin has been tested in more scenarios). Until it's uploaded to Roblox, you will need to insert this plugin file into your local plugins folder. This can be found by launching Studio, navigating to the Plugins tab, and clicking "Plugins Folder" on the left. Copy the `.rbxmx` file into that folder, then restart Studio.

## Step 4: Start the Python server

The last step before being able to use the tool is to start the Python server. Do this by running the following command: `py app.py` (use `python` if `py` doesn't work). The output log should look something like this:
![output](https://i.imgur.com/woJI7Oq.png)

## Step 5: Ready!

Everything should be ready now. In Studio, simply click on the "Reupload" plugin button to start.

![button](https://i.imgur.com/vLzoVPt.png)
