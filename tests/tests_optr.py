#!/usr/bin/env python

import unittest
from optr import Options

class OptrTestCase(unittest.TestCase):
    
    def setUp(self):
        self.default = dict(
            read = False,
            write = False,
            create = False,
            delete = False,
        )

        self.groups = dict(
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

        self.o = Options(groups=self.groups, default=self.default)

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

        self.adv_argmap = dict(
            optimise_level = optimise_opts
        )

        self.adv_default = {
            'optimise_level': 0,
            'sound': { 'LOUD': "very", 'REALTEK_DRIVER_0.0.1': '__SOUND_FILTER_ON' }
        }

        self.adv_groups = {
            'old-pc': {        
                'optimise_level': 1
            }
        }

    def test_defaults(self):
        q = {'write': False, 'read': False, 'create': False, 'delete': False}
        self.assertEqual(self.o, q)

    def test_resolve(self):
        q = {'write': False, 'read': True, 'create': False, 'delete': False}
        self.o._resolve("basic")
        self.assertEqual(self.o, q)

    def test_resolve_inheritance(self):
        q = {'write': True, 'read': True, 'create': True, 'delete': True}
        self.o._resolve("admin")
        self.assertEqual(self.o, q)
 
    def test_resolve_only_overwrite_new(self):
        # Resolving basic after admin should have no affect on any
        # option other than read, which stays True
        q = {'write': True, 'read': True, 'create': True, 'delete': True}
        
        self.o._resolve("admin")
        self.o._resolve("basic")
        
        self.assertEqual(self.o, q)
  
    def test_reset(self):
        q = {'write': False, 'read': True, 'create': False, 'delete': False}  
        
        self.o._resolve("admin")
        self.o._reset()._resolve("basic")
        self.assertEqual(self.o, q)
   
    def test_restore_default(self):
        self.groups.update(dict(
            blindeditor = dict(
                mixin = ['editor'],
                read = "__default__"    
            ),
        ))

        q = {'write': True, 'read': False, 'create': False, 'delete': False}
        
        self.o = Options(groups=self.groups, default=self.default)
        self.o._resolve('blindeditor')

        self.assertEquals(self.o, q)

    def test_advanced_arg(self):
        q = {'sound': {'REALTEK_DRIVER_0.0.1': '__SOUND_FILTER_ON', 'LOUD': 'very'}}
        self.o = Options(groups=self.adv_groups, default=self.adv_default, argmap=self.adv_argmap) 
        
        self.assertEquals(self.o, q)

    def test_advanced_arg_resolve(self):
        q = { 
            'sound': {'REALTEK_DRIVER_0.0.1': '__SOUND_FILTER_OFF', 'LOUD': 'very'}, 
            'graphics': {
                'light-density': 'sparse', 
                'draw-distance': 'LOW', 
                'textureQuality-xz': 0.001
            }
        }
        self.o = Options(groups=self.adv_groups, default=self.adv_default, argmap=self.adv_argmap)
        self.o._resolve("old-pc")
        
        self.assertEquals(self.o, q)

    def test_advanced_arg_resolve_only_overwrite_new(self):
        self.adv_groups.update({
            'not-so-old-pc': {
                'optimise_level': 1,
                'graphics': { 'light-density': "not-sparse" }
            }
        })

        q = { 
            'sound': {'REALTEK_DRIVER_0.0.1': '__SOUND_FILTER_OFF', 'LOUD': 'very'}, 
            'graphics': {
                'light-density': 'not-sparse', 
                'draw-distance': 'LOW', 
                'textureQuality-xz': 0.001
            }
        }

        self.o = Options(groups=self.adv_groups, default=self.adv_default, argmap=self.adv_argmap)
        self.o._resolve("not-so-old-pc")
        
        self.assertEquals(self.o, q)

if __name__ == '__main__':
    unittest.main()

