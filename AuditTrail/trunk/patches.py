"""
$Id: patches.py 1716 2006-10-29 19:23:31Z hazmat $
"""

# zope transaction manager is slightly idiotic about registering syncs on the txn
# manager only against the current thread id, add an option for doing better

import thread
import transaction
from transaction._transaction import Transaction
from transaction._manager import _new_transaction

class ObservableTxnManager(transaction.manager.__class__):
    """Thread-aware transaction manager.

    Each thread is associated with a unique transaction.
    """

    _global_syncs = []

    def begin(self):
        tid = thread.get_ident()
        txn = self._txns.get(tid)
        if txn is not None:
            txn.abort()

        synchs = self._synchs.get(tid)
        if synchs is None:
            from ZODB.utils import WeakSet
            synchs = self._synchs[tid] = WeakSet()
        if self._global_syncs:
            [synchs.add(gs) for gs in self._global_syncs]
        txn = self._txns[tid] = Transaction(synchs, self)
        _new_transaction(txn, synchs)
        return txn

    def get(self):
        tid = thread.get_ident()

        txn = self._txns.get(tid)
        if txn is None:
            synchs = self._synchs.get(tid)
            if synchs is None:                
                from ZODB.utils import WeakSet
                synchs = self._synchs[tid] = WeakSet()
            if self._global_syncs:
                [synchs.add(gs) for gs in self._global_syncs]
            txn = self._txns[tid] = Transaction(synchs, self)
        return txn

    def registerGlobalSynch( self, synch):
        self._global_syncs.append( synch )
        
transaction.manager.__class__ =  ObservableTxnManager
transaction.begin = transaction.manager.begin
transaction.get = transaction.manager.get
