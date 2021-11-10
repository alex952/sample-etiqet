"""FIX Application"""
import quickfix as fix
import quickfix42 as fix42
import logging
import time
from model.logger import setup_logger
__SOH__ = chr(1)

setup_logger('logfix', 'Logs/message.log')
logfix = logging.getLogger('logfix')

class Application(fix.Application):
    """FIX Application"""
    orderID = 0
    execID = 0


    def onCreate(self, sessionID):
        """onCreate"""
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        """onLogon"""
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        """onLogout"""
        print("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("(Admin) S >> %s" % msg)
        return

    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("(Admin) R << %s" % msg)
        return

    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("(App) S >> %s" % msg)
        return

    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("(App) R << %s" % msg)
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Mockup execution report for newordersingle"""
        beginString = fix.BeginString()
        msgType = fix.MsgType()
        message.getHeader().getField( beginString )
        message.getHeader().getField( msgType )

        symbol = fix.Symbol()
        side = fix.Side()
        ordType = fix.OrdType()
        orderQty = fix.OrderQty()
        price = fix.Price()
        clOrdID = fix.ClOrdID()

        message.getField( ordType )
        if ordType.getValue() != fix.OrdType_MARKET:
            raise fix.IncorrectTagValue( ordType.getField() )
#         message.getField( price )
# 
#         if price:
#             fix.TagNotDefinedForMessage( price.getField() )

        message.getField( symbol )
        message.getField( side )
        message.getField( orderQty )
        message.getField( clOrdID )


        def _generateExecReport(ordStatus, execType, clOrdID, orderId, execId, symbol, side, orderQty, price):
            executionReport = fix42.ExecutionReport()

            executionReport.setField( fix.ExecType(execType) )
            executionReport.setField( fix.OrdStatus(ordStatus) )
            executionReport.setField( fix.OrderID(orderId) )
            executionReport.setField( fix.ExecID(execId) )
            executionReport.setField( symbol )
            executionReport.setField( side )
            executionReport.setField( fix.OrderQty(orderQty.getValue()) )
            executionReport.setField( fix.CumQty(orderQty.getValue()) )
            executionReport.setField( fix.AvgPx(price.getValue()) )
            executionReport.setField( fix.LastPx(price.getValue()) )
            executionReport.setField( fix.LeavesQty(orderQty.getValue()) if ordStatus != fix.OrdStatus_FILLED else fix.LeavesQty(0) )
            executionReport.setField( clOrdID )
            executionReport.setField( orderQty )

            return executionReport


        orderId = self.genOrderID()
        execId = self.genExecID()
        pendingNew  = _generateExecReport(fix.OrdStatus_PENDING_NEW, fix.ExecType_PENDING_NEW, clOrdID, "0000", "0000", symbol, side, orderQty, fix.Price(0.0))
        new         = _generateExecReport(fix.OrdStatus_NEW, fix.ExecType_NEW, clOrdID, orderId, execId, symbol, side, orderQty, fix.Price(1.3))
        filled      = _generateExecReport(fix.OrdStatus_FILLED, fix.ExecType_FILL, clOrdID, orderId, execId, symbol, side, orderQty, fix.Price(1.3))

        try:
            fix.Session.sendToTarget( pendingNew, sessionID )
            fix.Session.sendToTarget( new, sessionID )
            fix.Session.sendToTarget( filled, sessionID )
        except fix.SessionNotFound as e:
            return

    def genOrderID(self):
        self.orderID += 1
        return str(self.orderID).zfill(5)

    def genExecID(self):
        self.execID += 1
        return str(self.execID).zfill(5)

    def run(self):
        """Run"""
        while 1:
            time.sleep(2)
