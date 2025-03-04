"""
Created on Dec 7, 2017

@author: Tim
"""

import unittest
import os
from os.path import join

from praatio import tgio
from praatio import dataio
from praatio import kgio
from praatio import audioio


class IOTests(unittest.TestCase):
    """Testing input and output"""

    def __init__(self, *args, **kargs):
        super(IOTests, self).__init__(*args, **kargs)

        cwd = os.path.dirname(os.path.realpath(__file__))
        root = os.path.split(cwd)[0]
        self.dataRoot = join(root, "files")
        self.outputRoot = join(self.dataRoot, "io_test_output")

    def test_openTextgrid(self):
        tgFN = join(self.dataRoot, "mary.TextGrid")

        tg = tgio.openTextgrid(tgFN)
        tier = tg.tierDict["word"]
        numEntries = len(tier.entryList)

        self.assertEqual(4, numEntries)

    def test_openTextgrid_with_readRaw(self):
        tgFN = join(self.dataRoot, "mary.TextGrid")

        tg = tgio.openTextgrid(tgFN, True)
        tier = tg.tierDict["word"]
        numEntries = len(tier.entryList)

        self.assertEqual(6, numEntries)

    def test_shift(self):
        """Testing adjustments to textgrid times"""
        tgFN = join(self.dataRoot, "mary.TextGrid")

        tg = tgio.openTextgrid(tgFN)
        shiftedTG = tg.editTimestamps(0.1, True)
        unshiftedTG = shiftedTG.editTimestamps(-0.1, True)

        self.assertTrue(tg == unshiftedTG)

    def test_insert_delete_space(self):
        """Testing insertion and deletion of space in a textgrid"""
        tgFN = join(self.dataRoot, "mary.TextGrid")

        tg = tgio.openTextgrid(tgFN)
        stretchedTG = tg.insertSpace(1, 1, "stretch")
        unstretchedTG = stretchedTG.eraseRegion(1, 2, doShrink=True)

        self.assertTrue(tg == unstretchedTG)

    def test_rename_tier(self):
        """Testing renaming of tiers"""

        tgFN = join(self.dataRoot, "mary.TextGrid")

        tg = tgio.openTextgrid(tgFN)

        tg.renameTier("phone", "candy")

        self.assertTrue("phone" not in tg.tierNameList)
        self.assertTrue("candy" in tg.tierNameList)

    def test_mintimestamp_behaviour(self):
        userEntryList = [[0.4, 0.6, "A"], [0.8, 1.0, "E"], [1.2, 1.3, "I"]]

        # By default, the min and max timestamp values come from the entry list
        tier = tgio.IntervalTier("test", userEntryList)
        self.assertEqual(0.4, tier.minTimestamp)
        self.assertEqual(1.3, tier.maxTimestamp)

        # The user can specify the min and max timestamp
        tier = tgio.IntervalTier("test", userEntryList, 0.2, 2.0)
        self.assertEqual(0.2, tier.minTimestamp)
        self.assertEqual(2.0, tier.maxTimestamp)

        # When the user specified min/max timestamps are less/greater
        # than the min/max specified in the entry list, use the values
        # specified in the entry list
        tier = tgio.IntervalTier("test", userEntryList, 1.0, 1.1)
        self.assertEqual(0.4, tier.minTimestamp)
        self.assertEqual(1.3, tier.maxTimestamp)

    def setUp(self):
        if not os.path.exists(self.outputRoot):
            os.mkdir(self.outputRoot)


if __name__ == "__main__":
    unittest.main()
