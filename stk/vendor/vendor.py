"""Support Toolkit vender.py
@package SupportToolkit
@copyright (c) 2012 phpBB Group
@license http://opensource.org/licenses/gpl-2.0.php GNU General Public License v2

This utility copies all vendor files that are required by the Support Toolkit
into their correct locations. This tool expects that the vendor repositories
are already checked out.
"""
import argparse;
from os import chdir, getcwd, makedirs, remove;
from os.path import dirname, exists, isdir;
from shutil import copy2, copytree, rmtree;
from subprocess import PIPE, Popen;
import types;

def getphpBBFileList():
	return [
		[
			"",
			[
				"composer.json",
				"composer.lock",
			],
			"phpBB/"
		],
		[
			"adm/images/",
			[
				"arrow_down.gif",
				"arrow_left.gif",
				"arrow_right.gif",
				"bg_button.gif",
				"bg_tabs1.gif",
				"bg_tabs2.gif",
				"corners_left.gif",
				"corners_right.gif",
				"gradient2b.gif",
				"innerbox_bg.gif",
				"phpbb_logo.gif",
				"toggle.gif",
			],
			"view/images/"
		],
		[
			"adm/style/admin.css",
			"view/theme/admin.css"
		],
		[
			"includes/",
			[
				"constants.php",
				"functions.php",
				"session.php",
				"startup.php",
				"user.php",
			],
			"phpBB/includes/"
		],
		[
			"includes/auth/",
			"phpBB/includes/auth/"
		],
		[
			"includes/cache/",
			[
				"factory.php",
				"service.php",
			],
			"phpBB/includes/cache/"
		],
		[
			"includes/cache/driver/",
			"phpBB/includes/cache/driver/"
		],
		[
			"includes/config/",
			[
				"config.php",
				"db.php",
			],
			"phpBB/includes/config/"
		],
		[
			"includes/db/",
			"phpBB/includes/db/"
		],
		[
			"includes/request/",
			"phpBB/includes/request/"
		],
		[
			"includes/style/",
			[
				"path_provider.php",
				"path_provider_interface.php",
				"resource_locator.php",
				"style.php",
				"template.php",
				"template_compile.php",
				"template_context.php",
				"template_filter.php",
				"template_renderer.php",
				"template_renderer_include.php",
			],
			"phpBB/includes/style/"
		],
		[
			"includes/utf/",
			[
				"utf_normalizer.php",
				"utf_tools.php",
			],
			"phpBB/includes/utf/"
		],
		[
			"includes/utf/data/",
			"phpBB/includes/utf/data/"
		]
	];

def _copy(src, dest, update=False):
	if (exists(dest) and update == False):
		print ('Skipping: ' + src + ' (destination already exists)');
		return False;

	print (('Copying: ' if update == False else 'Force copying: ') + src + ' to: ' + dest);
	if isdir(src):
		if (exists(dirname(dest)) and update == True):
			rmtree(dest);

		copytree(src, dest);
	else:
		if not exists(dirname(dest)):
			makedirs(dirname(dest));
		elif (exists(dest) and update == True):
			remove(dest);

		copy2(src, dest);

	return True;

def main():
	cwd = getcwd();

	parser = argparse.ArgumentParser(description='Script that copies vendor files to the correct location into the Support Toolkit tree. This script assumes that the vendor submodules are already checked out.');
	parser.add_argument(
		"-u",
		"--update",
		dest="update",
		action="store_true",
		help="Update files, setting this parameter will force the script to overwrite the files if they already exist"
	);
	args = parser.parse_args();

	# phpBB files
	basesrc		= './stk/vendor/phpBB/phpBB/';
	basedest	= './stk/';

	for file in getphpBBFileList():
		if isinstance(file[1], types.ListType):
			for f in file[1]:
				_copy(basesrc + file[0] + f, basedest + file[2] + f, args.update);
		else:
			_copy(basesrc + file[0], basedest + file[1], args.update);

	# Pimple
	_copy ('./stk/vendor/Pimple/lib/Pimple.php', './stk/core/DI/Pimple.php', args.update);

	# MODX
	_copy ('./stk/vendor/MODX/modx.prosilver.en.xsl', './contrib/modx.prosilver.en.xsl', args.update);

	# Finally install and run composer in 'stk/phpBB/'
	chdir('./stk/phpBB/');
	p1 = Popen(['curl', '-s', 'http://getcomposer.org/installer'], stdout=PIPE);
	p2 = Popen(['php'], stdin=p1.stdout, stdout=PIPE);
	p1.stdout.close();
	p2.communicate()[0];

	p3 = Popen(['php', 'composer.phar', 'install'], stdout=PIPE);
	p3.stdout.close();
	chdir(cwd);

if __name__ == "__main__":
	main();
