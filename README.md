This is a solution for a problem that has still, to this day, remained unsolved because of the incompetency and blind ignorance of a group of "genius" individuals who would refer to themselves as part of a "brilliancy" called MicroSoft. Which is of course the reason for being a straight up cunt to people who have, in good faith, invested their money into a product that they expected to be complete and fully functional. Yet here we are, instead of fixing things, that are actually necessary, you imbeciles decide to bloat the system with shite that no one will either realise it exists or and most likely will never use.  
Still wondering? Not a problem, there you have it, halfwits:
[here](https://www.makeuseof.com/microsoft-windows-11-file-explorer-ads/),
[here](https://www.reddit.com/r/Windows11/comments/qs96dp/ayy_microsoft_can_you_please_stop_widgets_from/),
[here](https://www.reddit.com/r/pcgaming/comments/cz17bw/psa_check_your_cortana_usage_right_now_if_its_up/),
[here](https://www.reddit.com/r/Windows10/comments/f09184/how_to_block_bing_search_in_windows_10_start_menu/),
[here](https://answers.microsoft.com/en-us/windows/forum/all/windows-10-updates-during-active-hours-while-im/07dee705-e3e8-43af-9b6c-b6fdf91b9005),
[here](https://www.reddit.com/r/Windows10/comments/ofkmzm/why_arent_windows_updates_and_telemetry_data_opt/)
and
[here](https://np.reddit.com/r/privacy/comments/cici51/how_much_does_microsoft_spy_on_its_users_via/ev4pvxb/).  
For the pyromaniacs, we've got a solution like [this](https://github.com/bmrf/tron/blob/master/resources/stage_4_repair/disable_windows_telemetry/purge_windows_10_telemetry.bat).
> TLDR: MicroSoft can, yet again, go fuck themselves

## The fuck is this then?
<p align="center">
  <img src="https://user-images.githubusercontent.com/60236942/191240641-540820dd-3010-4bc7-aa1e-81c526600440.png?raw=true"/>
</p>

I'm glad you asked. Picture this, you're at work. You're booting up your computer and you had a ton of applications open yesterday, now you'd like them to be at the same spot where they were, right? Wouldn't that be nice? We both know the answer to that. But since Windows has the memory of a middle aged chimp and no idea what an application window is, it just throws everything up like an anorexic who just shoveled in a slice of banana cake and threw it up the minute the second they realised it was them in the mirror. Which is why I've created a script, which in layman's terms, takes a screenshot of your current state in the desktop and saves it into a configuration file which can then be loaded into the script to set up everything the way it was. Simple, innit? Yet the nobs at a certain company could not make something like this and integrate it to the system. Nothing new this day and age.
## Installation
Get [python](https://www.python.org/downloads/release/python-396/)  
``pip3 install pipenv`` This bit creates a virtual environment, which is used to safely run the script  
``pipenv install`` Installs the required packages from the Pipfile
## Usage
``pipenv run python winporn.py --load settings_file.xml`` Loads the settings file and initiates the setup accordingly  
``pipenv run python winporn.py --save my_desktop.xml`` Saves the current desktop setup to a specified file on the disk  
>Keep the settings files in the same folder with the script, it won't run otherwise (no point really)
## Settings files
Based on the [XML](https://en.wikipedia.org/wiki/XML) format, can be easily modified according to specified needs.  
They are validated by the script and the [XSD](https://en.wikipedia.org/wiki/XML_Schema_(W3C)) file.
