# Optr

Optr allows you to create CSS-esque inheritance for options in Python. It allows you to define groups of options that can inherit from one another, and provides a way to tame complex option hierarchies. 

At its most basic form it allows for the recursive merging of dictionaries, however it also provides advanced functionality such as inheritance, mapping pseudo-arguments to groups of options, and restoration of default values.

# BASIC USAGE

	from optr import Options

	# Don't allow any features by default
	default = dict(
		read = False,
		write = False,
		create = False,
		delete = False,
	)

	groups = dict(
		# A basic user can read files
		basic = dict(
			read = True,
		),
		# An editor can do everything basic can do, but also write.
		editor = dict(
			mixin = ['basic'],
			write = True
		),
		# An admin can do everything an editor can do, but also create/delete
		admin = dict(
			mixin = ['editor'],
			create = True,
			delete = True,
		),
	)

	o = Options(groups=groups, default=default)

	# Options begins with all the defaults

	print o
	# {write': False, 'read': False, 'create': False, 'delete': False}

	# This will resolve the options for the group basic, it 
	# gets read from the group, then the rest remain defaults.

	print o._resolve("basic")
	# {'write': False, 'read': True, 'create': False, 'delete': False}

	# This will resolve the group admin, as we have already resolved
	# basic, any options set by basic (ignoring the fact in this example
	# admin inherits basic through editor) will remain as they are unless 
	# admin overwrites them.

	print o._resolve("admin")
	# {'write': True, 'read': True, 'create': True, 'delete': True}

	# This will resolve the group basic, as we have already resolved admin
	# read is set to True, and the rest of the options remain untouched.

	print o._resolve("basic")
	# {'write': True, 'read': True, 'create': True, 'delete': True}

	# If we wanted to demote this user from an admin to a basic user, 
	# we can create a new options object, or use _reset

	print o._reset()._resolve("basic")
	# {'write': False, 'read': True, 'create': False, 'delete': False}

# ADVANCED USAGE

## Restoring defaults

	groups.update(dict(
		
		# We want a new blindeditor, who can do everything an editor
		# can do, but cannot read articles. You can inherit editor,
		# then set read to False, or you can set read to __default__
		# which will restore read to its default value.

		blindeditor = dict(
			mixin = ['editor'],
			read = "__default__"	
		),
	))

	o = Options(groups=groups, default=default)

	print o._resolve('blindeditor')
	# {'write': True, 'read': False, 'create': False, 'delete': False}

## Advanced arguments

	# The argument map lets you map options to other options,
	# a way of creating nice syntactic sugar so that option
	# groups can be easy and nice to write, but the underlying
	# options needed by your program may be messy

	# This is some ugly function that sets some hypothetical 
	# options based on the level passed into the function to 
	# optimise a program

	def optimise_opts(level):
		if level == 1:
			return {
				'graphics': {
					'light-density': "sparse",
					'draw-distance': "LOW",
					'textureQuality-xz': 0.001,
				},
				'sound': {
					'REALTEK_DRIVER_0.0.1': "__SOUND_FILTER_OFF"
				}
			}
		else:
			return {}

	# Now we map a nice command, optimise_level to this function
	argmap = dict(
		optimise_level = optimise_opts
	)

	# Set a default
	default = {
		'optimise_level': 0,
		'sound': { 'LOUD': "very", 'REALTEK_DRIVER_0.0.1': '__SOUND_FILTER_ON' }
	}

	# Create our group
	groups = {
		'old-pc': {		
			# Now we can simply set optimise_level in any groups 
			# and we can forget the underlying complexity and 
			# inconsistency of the arguments. Argument maps can 
			# be used even for just simple aliasing if preferred.

			'optimise_level': 1
		}
	}

	o = Options(groups=groups, default=default, argmap=argmap)

	print o
	# {'sound': {'REALTEK_DRIVER_0.0.1': '__SOUND_FILTER_ON', 'LOUD': 'very'}}

	print o._resolve('old-pc')
	# { 
	#	'sound': {'REALTEK_DRIVER_0.0.1': '__SOUND_FILTER_OFF', 'LOUD': 'very'}, 
	#	'graphics': {
	#		'light-density': 'sparse', 
	#		'draw-distance': 'LOW', 
	#		'textureQuality-xz': 0.001
	#	}
	# }

	#
	# Even using a complex argument map, the underlying options
	# can still be overwritten and modified if required.
	#

	groups.update({
		'not-so-old-pc': {

			# This will change just list-density to not-sparse, 
			# it will not remove draw-distance, or textureQuality-xz 
			# from graphics
			'optimise_level': 1,
			'graphics': { 'light-density': "not-sparse" }
		}
	})

	o = Options(groups=groups, default=default, argmap=argmap)
	print o._resolve('not-so-old-pc')
	# { 
	#	'sound': {'REALTEK_DRIVER_0.0.1': '__SOUND_FILTER_OFF', 'LOUD': 'very'}, 
	#	'graphics': {
	#		'light-density': 'not-sparse', 
	#		'draw-distance': 'LOW', 
	#		'textureQuality-xz': 0.001
	#	}
	# }

# Testing

	adamcw:tests adamcw$ coverage run ./tests_optr.py 
	.........
	----------------------------------------------------------------------
	Ran 10 tests in 0.002s

	OK

	adamcw:tests adamcw$ coverage report -m
	Name                                     Stmts   Miss  Cover   Missing
	----------------------------------------------------------------------
	/lib/python/optr/__init__					1       0   100%   
	/lib/python/optr/optr						51      0   100%   
	tests_optr                                  62      0   100%   
	----------------------------------------------------------------------
	TOTAL                                      114      0   100%  

# License

Copyright (C) 2012 Adam Whiteside

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

