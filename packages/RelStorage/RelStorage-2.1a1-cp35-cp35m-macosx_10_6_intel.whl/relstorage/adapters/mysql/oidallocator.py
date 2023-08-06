##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
IOIDAllocator implementations.
"""

from __future__ import absolute_import

from ..oidallocator import AbstractOIDAllocator
from ..interfaces import IOIDAllocator
from zope.interface import implementer

from perfmetrics import metricmethod

@implementer(IOIDAllocator)
class MySQLOIDAllocator(AbstractOIDAllocator):

    def set_min_oid(self, cursor, oid):
        """Ensure the next OID is at least the given OID."""
        n = (oid + 15) // 16
        cursor.execute("REPLACE INTO new_oid VALUES(%s)", (n,))

    @metricmethod
    def new_oids(self, cursor):
        """Return a sequence of new, unused OIDs."""
        stmt = "INSERT INTO new_oid VALUES ()"
        cursor.execute(stmt)
        # This is a DB-API extension. Fortunately, all
        # supported drivers implement it. (In the past we used
        # cursor.connection.insert_id(), which was specific to MySQLdb)
        n = cursor.lastrowid

        if n % 1000 == 0:
            # Clean out previously generated OIDs.
            stmt = "DELETE FROM new_oid WHERE zoid < %s"
            cursor.execute(stmt, (n,))
        return self._oid_range_around(n)
