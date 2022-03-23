<img src="resources/icon.png" align="right" height="84" />

# Bulk Audio Reupload Helper [![License](https://img.shields.io/github/license/the-sink/roblox-reuploader)](https://github.com/the-sink/roblox-reuploader/blob/main/LICENSE) [![Issues](https://img.shields.io/github/issues/the-sink/roblox-reuploader)](https://github.com/the-sink/roblox-reuploader/issues)

-----

**As of March 22nd, this tool is unable download assets that fail the newly added permissions check.** It may still function under specific circumstances (i.e. you are looking to migrate audio on a group game that you have uploaded to your personal account), but in many cases is now useless. Anyone who did not migrate in time or had technical issues preventing them from doing so will have to find replacement audio or wait until they release the ability to set audio as Public again.

-----

As many are already well aware of, [Roblox is making it so that audio above 5.5 seconds can only be used if you are the uploader](https://devforum.roblox.com/t/action-needed-upcoming-changes-to-asset-privacy-for-audio/1701697) on March 22nd, 2022. This tool's objective is to ease the process of transitioning your game over, by automatically collecting all audio that requires migration and automatically re-uploading it into your profile (or the group, if you're running this in a group game.)

# Warnings

* **Roblox may very soon be implementing audio permissions that make this asset re-upload process unneccesary.** As some have noted, new options have appeared (but are currently disabled) in the configuration page for audio assets:
![options](https://i.imgur.com/zcCI3gM.png)
It is at your discretion whether you think bulk uploading audio to your account will be neccesary.

* **This tool is experimental.** I developed it fairly quickly and have not had ample time yet to thoroughly test it. If you are migrating a game with a lot of audio assets, please closely monitor the profile that audio is being uploaded to and ensure nothing is going wrong. If you notice any unusual errors or behavior, feel free to contact me or submit an issue.

* **Make sure you have the quota available to upload all of the audio.** Another change as a result of this is that audio uploads are now free - but every user has a monthly quota that is dependent on a few factors (such as whether you are ID verified.) You can check your quota by visiting the audio upload page on the website. The plugin will display the **maximum** total number of assets it intends to upload on-screen and will require you to confirm this. Keep in mind, this number is not *neccesarily* the final amount of assets that will be uploaded, as it keeps a running list of all of the assets it has previously uploaded (these are used instead of uploading duplicates). Invalid/copyrighted assets and HTTP errors can affect this as well, of course.

* **Use at your own risk.** Using this tool means uploading a bunch of audio assets to **your account** all at once, and there is potential for your account to be moderated as result. If you are worried, examine the audio that will be reuploaded to make sure there are no obvious rule-breaking/copyrightable assets.

**Known issue:** The server script currently saves a list of all files it has migrated to `uploaded_id_list.json`. This file **does not** record what profile these assets have been uploaded to (i.e. if it was uploaded to your profile, or a specific group you're in if editing a group game). This means, for example, if you used this tool in a game on your profile to migrate audio that *also* exists in a group game you are about to migrate, the **already re-uploaded files** that have been uploaded to your account will be used on the group game, thus failing to meet the new permissions checks being imposed on March 22nd. This will be fixed soon.
<!-- Perhaps move this issue part somewhere else? Just doesn't feel right to be here... - ATPStorages -->

# Prerequisites
## Python

The included reupload server is written in Python and will be required at all times while using this program.

You can download the latest version of Python [here](**https://www.python.org/**). If you are on Windows, installing Python through the Microsoft Store is also an option.
The version I have personally tested this on is **3.10.2**.

If you are installing it for the first time, it is likely you will need to restart your system (or relog,) and whatever terminals you have open at the moment. 

## Step 1: Download server

First, download this repository. You can click [here](https://github.com/the-sink/roblox-reuploader/archive/refs/heads/main.zip), or you can use the GitHub interface:

![Step1](https://i.imgur.com/OW7CcFW.png)

Unzip the contents into a folder somewhere **safe** (there is a file the server will create that you wlll not want to lose).

Open a command line window in the same folder as the repo's files. One quick way to do this is by clicking on the address bar in Explorer and entering `cmd`.

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

The companion plugin is available [here](https://www.roblox.com/library/9106046275/Bulk-Audio-Reupload-Helper) to install. This plugin will send the server a list of all IDs that need to be reuploaded, and replaces all old IDs with the new ones in studio once the uploads have completed.

A copy of the required plugin exists in the repo, called `AudioReupload.rbxmx`, if you wish to use a local copy instead.

## Step 4: Start the Python server

The last step before being able to use the tool is to start the Python server. Do this by running the following command: `py app.py` (use `python` if `py` doesn't work.) The output log should look something like this:
![output](https://i.imgur.com/woJI7Oq.png)

## Step 5: Ready!

Everything should be ready now. In Studio, simply click on the "Reupload" plugin button to start.

![button](https://i.imgur.com/vLzoVPt.png)

Make sure not to delete or misplace `uploaded_id_list.json`. This is the file that prevents the server from uploading duplicate audio, as it stores a running list of all reuploads it has completed (old ID and new ID). If this file is lost, any audio that needs to be migrated that was *previously* already migrated by the tool will need to be uploaded again, wasting upload quota.
