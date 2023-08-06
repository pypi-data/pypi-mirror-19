import astrogear as ag
import os
from PyQt4.QtGui import *


def test_NullEditor():
    app = ag.get_QApplication()
    obj = ag.NullEditor()


def test_Parameter():
    app = ag.get_QApplication()
    obj = ag.Parameter()


def test_Parameters():
    app = ag.get_QApplication()
    obj = ag.Parameters()


# def test_PythonHighlighter():
#     app = ag.get_QApplication()
#     obj = ag.PythonHighlighter()


# def test_SignalProxy():
#     app = ag.get_QApplication()
#     obj = ag.SignalProxy()


def test_VerticalLabel():
    app = ag.get_QApplication()
    obj = ag.VerticalLabel(ag.XLogDialog())


def test_WBase():
    app = ag.get_QApplication()
    obj = ag.WBase(ag.XLogDialog())


def test_WChooseSpectrum():
    app = ag.get_QApplication()
    obj = ag.WChooseSpectrum(ag.XLogDialog())


def test_WCollapsiblePanel():
    app = ag.get_QApplication()
    obj = ag.WCollapsiblePanel(ag.XLogDialog())


def test_WDBRegistry():
    app = ag.get_QApplication()
    obj = ag.WDBRegistry(ag.XLogDialog())


# def test_WParametersEditor():
#     app = ag.get_QApplication()
#     obj = ag.WParametersEditor(None, ag.Parameters([["field0", {"value": 0}], ["field1", {"value": 1}]]))


def test_WSelectDir():
    app = ag.get_QApplication()
    obj = ag.WSelectDir(ag.XLogMainWindow())


def test_WSelectFile():
    app = ag.get_QApplication()
    obj = ag.WSelectFile(ag.XLogMainWindow())


def test_XFileMainWindow():
    app = ag.get_QApplication()
    obj = ag.XFileMainWindow()


def test_XLogDialog():
    app = ag.get_QApplication()
    obj = ag.XLogDialog()


def test_XLogMainWindow():
    app = ag.get_QApplication()
    obj = ag.XLogMainWindow()


# def test_XParametersEditor():
#     app = ag.get_QApplication()
#     obj = ag.XParametersEditor()


# def test_are_you_sure():
#     app = ag.get_QApplication()
#     obj = ag.are_you_sure("msg")


# def test_check_return_space():
#     app = ag.get_QApplication()
#     obj = ag.check_return_space()

def test_enc_name():
    app = ag.get_QApplication()
    obj = ag.enc_name("name")


def test_enc_name_descr():
    app = ag.get_QApplication()
    obj = ag.enc_name_descr("name", "descr")


def test_format_title0():
    app = ag.get_QApplication()
    obj = ag.format_title0("aaa")


def test_format_title1():
    app = ag.get_QApplication()
    obj = ag.format_title1("aaa")


def test_format_title2():
    app = ag.get_QApplication()
    obj = ag.format_title2("aaa")


def test_get_QApplication():
    app = ag.get_QApplication()
    obj = ag.get_QApplication()


# TODO test non-existing icons
def test_get_icon():
    app = ag.get_QApplication()
    assert isinstance(ag.get_icon("document-open"), QIcon)
    # Not like this, always returns a QIcon assert ag.get_icon("aaaaaaaa") == None


def test_get_matplotlib_layout():
    app = ag.get_QApplication()
    obj = ag.get_matplotlib_layout(QWidget())


def test_get_window_title():
    app = ag.get_QApplication()
    obj = ag.get_window_title("prefix")


def test_keep_ref():
    app = ag.get_QApplication()
    obj = ag.keep_ref(QWidget())


def test_nerdify():
    app = ag.get_QApplication()
    obj = ag.nerdify(QWidget())


def test_place_center():
    app = ag.get_QApplication()
    obj = ag.place_center(QMainWindow())


def test_place_left_top():
    app = ag.get_QApplication()
    obj = ag.place_left_top(QMainWindow())


def test_reset_table_widget():
    app = ag.get_QApplication()
    t = QTableWidget()
    obj = ag.reset_table_widget(t, 10, 10)


# def test_show_edit_form():
#     app = ag.get_QApplication()
#     obj = ag.show_edit_form()
#
#
# def test_show_error():
#     app = ag.get_QApplication()
#     obj = ag.show_error("test")
#
#
# def test_show_message():
#     app = ag.get_QApplication()
#     obj = ag.show_message("test")
#
#
# def test_show_warning():
#     app = ag.get_QApplication()
#     obj = ag.show_warning("test")


def test_snap_left():
    app = ag.get_QApplication()
    obj = ag.snap_left(QMainWindow())


def test_snap_right():
    app = ag.get_QApplication()
    obj = ag.snap_right(QMainWindow())


# def test_style_checkboxes():
#     app = ag.get_QApplication()
#     obj = ag.style_checkboxes()


# def test_style_widget_changed():
#     app = ag.get_QApplication()
#     obj = ag.style_widget_changed()
#
#
# def test_style_widget_valid():
#     app = ag.get_QApplication()
#     obj = ag.style_widget_valid()


def test_table_info_to_parameters(tmpdir):
    fn = os.path.join(str(tmpdir), "testdb.sqlite")
    conn = ag.get_conn(fn)
    conn.execute("create table test (id integer primary key, name text)")
    ti = ag.get_table_info(conn, "test")

    app = ag.get_QApplication()
    obj = ag.table_info_to_parameters(ti)

    assert ti == {'id': {'cid': 0,
                         'name': 'id',
                         'type': 'integer',
                         'notnull': 0,
                         'dflt_value': None,
                         'pk': 1},
                  'name': {'cid': 1,
                           'name': 'name',
                           'type': 'text',
                           'notnull': 0,
                           'dflt_value': None,
                           'pk': 0}}


