"""Run with python -m unittest discover -s tools -p 'test_*.py'."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import install_mod
import validate_mod
import prepare_runtime_test


class ValidationTests(unittest.TestCase):
    def test_physics_origin_rejects_zero_height_before_suspension_compression(self):
        unsafe = 'model { offset = 0 .65 0, } suspensionRestLength = .18, wheel FrontLeft { offset = .77 -.32 1.43, radius = .33, }'
        self.assertTrue(validate_mod.physics_origin_errors(unsafe))
        self.assertEqual(validate_mod.physics_origin_errors(unsafe.replace('0 .65 0', '0 0 0')), [])

    def test_entry_area_rejects_target_inside_native_navigation_padding(self):
        unsafe = 'extents = 1.92 0.95 4.80, area SeatFrontLeft { xywh = 1.20 0 .60 .80, }'
        self.assertTrue(validate_mod.interaction_clearance_errors(unsafe))
        safe = unsafe.replace('1.20 0', '1.45 0')
        self.assertEqual(validate_mod.interaction_clearance_errors(safe), [])

    def test_braces_ignore_comments_and_strings(self):
        self.assertTrue(validate_mod.balanced('module Base { /* } */ value = "{" , }'))
        self.assertFalse(validate_mod.balanced('module Base { } }'))

    def test_incomplete_package_reports_errors(self):
        with tempfile.TemporaryDirectory() as folder:
            errors, _ = validate_mod.validate(Path(folder))
            self.assertTrue(any('mod.info' in error for error in errors))

    def test_reference_cannot_escape_media(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                validate_mod.media_path(Path(folder), '../private')


class InstallerTests(unittest.TestCase):
    def test_never_overwrites_unowned_mod_even_with_update(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'source'
            source.mkdir()
            target = root / 'mods' / 'Javelin73PC'
            target.mkdir(parents=True)
            (target / 'unrelated.txt').write_text('preserve')
            with self.assertRaises(ValueError):
                install_mod.install(source, target, update=True)
            self.assertEqual((target / 'unrelated.txt').read_text(), 'preserve')

    def test_update_backs_up_owned_mod_and_excludes_docs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'source'
            (source / '42').mkdir(parents=True)
            (source / '42' / 'mod.info').write_text('id=Javelin73PC')
            (source / '42' / 'AGENTS.md').write_text('development only')
            target = root / 'mods' / 'Javelin73PC'
            install_mod.install(source, target)
            self.assertFalse((target / '42' / 'AGENTS.md').exists())
            (source / '42' / 'mod.info').write_text('id=Javelin73PC\nname=updated')
            backup = install_mod.install(source, target, update=True)
            self.assertEqual((backup / '42' / 'mod.info').read_text(), 'id=Javelin73PC')
            self.assertIn('updated', (target / '42' / 'mod.info').read_text())

    def test_wrong_destination_name_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                install_mod.install(Path(folder), Path(folder) / 'OtherMod')


class RuntimePreparationTests(unittest.TestCase):
    def test_visual_final_fresh_cache_does_not_fabricate_reload_record(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            cache = root/'build'/'fresh-final'
            with patch.object(prepare_runtime_test, 'ROOT', root), patch.object(prepare_runtime_test, 'install'):
                prepare_runtime_test.prepare(cache, auto_start=True, save_test=True, visual_final=True)
            self.assertFalse((cache/'Lua'/'j73-persistence-test.txt').exists())
            hook = (cache/'mods/Javelin73PC/42/media/lua/client/J73RuntimeAudit.lua').read_text()
            self.assertIn('if J73GameplayAudit.resuming then\n        J73GameplayAudit.verifyReload(true)\n        return\n    end', hook)
            self.assertNotIn('__VISUAL_FINAL__', hook)

    def test_visual_final_requires_explicit_save_workflow_before_mutation(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder)/'untouched'
            with self.assertRaises(ValueError):
                prepare_runtime_test.prepare(target, visual_final=True)
            self.assertFalse(target.exists())

    def test_persistence_cannot_target_user_save_or_unmarked_cache(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            outside = root / 'Saves'
            existing = root / 'build' / 'existing'
            existing.mkdir(parents=True)
            sentinel = existing / 'preserve.txt'
            sentinel.write_text('keep')
            with patch.object(prepare_runtime_test, 'ROOT', root):
                for target in (outside, existing):
                    with self.assertRaises(ValueError):
                        prepare_runtime_test.prepare(target, save_test=True)
            self.assertFalse(outside.exists())
            self.assertEqual(sentinel.read_text(), 'keep')

    def test_auto_start_is_explicit_and_scoped_to_disposable_hook(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with patch.object(prepare_runtime_test, 'ROOT', root), patch.object(prepare_runtime_test, 'install'):
                for auto_start in (False, True):
                    cache = root / 'build' / str(auto_start)
                    prepare_runtime_test.prepare(cache, auto_start=auto_start)
                    hook = cache / 'mods/Javelin73PC/42/media/lua/client/J73RuntimeAudit.lua'
                    source = hook.read_text()
                    self.assertIn('if ' + str(auto_start).lower() + ' then\n    Events.OnMainMenuEnter.Add', source)
                    self.assertNotIn('__AUTO_START__', source)
                    self.assertTrue((cache / 'mods/reset-mods-42_00.txt').is_file())
            self.assertFalse((root / 'Javelin73PC').exists())


if __name__ == '__main__':
    unittest.main()
