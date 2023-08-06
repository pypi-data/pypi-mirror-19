import pytest
import os
import astrogear as ag


def test_get_conn(tmpdir):
    fn = os.path.join(str(tmpdir), "testdb.sqlite")
    conn = ag.get_conn(fn)


def test_conn_is_open(tmpdir):
    fn = os.path.join(str(tmpdir), "testdb.sqlite")
    conn = ag.get_conn(fn)
    assert ag.conn_is_open(conn)



def test_get_table_names(tmpdir):
    fn = os.path.join(str(tmpdir), "testdb.sqlite")
    conn = ag.get_conn(fn)
    conn.execute("create table test (id integer primary key, name text)")
    names = ag.get_table_names(conn)
    assert names == ["test"]


def test_cursor_to_data_header(tmpdir):
    fn = os.path.join(str(tmpdir), "testdb.sqlite")
    conn = ag.get_conn(fn)
    conn.execute("create table test (id integer primary key, name text)")
    conn.executemany("insert into test values (?, ?)", [[1, "Joao"], [2, "Maria"]])
    cursor = conn.execute("select * from test")
    data, header = ag.cursor_to_data_header(cursor)
    data1 = [list(x) for x in data]
    assert data1 == [[1, "Joao"], [2, "Maria"]]
    assert header == ["id", "name"]


def test_get_table_info(tmpdir):
    fn = os.path.join(str(tmpdir), "testdb.sqlite")
    conn = ag.get_conn(fn)
    conn.execute("create table test (id integer primary key, name text)")
    ti = ag.get_table_info(conn, "test")
    assert ti == ag.TableInfo((("id", ag.MyDBRow([('cid', 0), ('name', 'id'), ('type', 'integer'), ('notnull', 0), ('dflt_value', None), ('pk', 1)])),
                               ("name", ag.MyDBRow([('cid', 1), ('name', 'name'), ('type', 'text'), ('notnull', 0), ('dflt_value', None), ('pk', 0)])),
                             ))
