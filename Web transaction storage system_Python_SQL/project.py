


import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, Sequence, create_engine
from flask import Flask, request,  redirect, render_template,session,flash,jsonify



# class JSONEncoder(_JSONEncoder):
#     def default(self, o):
#         if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
#             print(dict(o))
#         else:
#             print("CAN NOT SERREALIZE")
#
#
# class Flask(Flask):
#     json_encoder = JSONEncoder



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mrsoft.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import json




class Users(db.Model):
    __tablename__ = 'user'
    id = Column(Integer,autoincrement=True,primary_key=True)
    username = Column(String(20))
    password = Column(String(64))
    type =  Column(String(20))
    role = Column(String(20))

    def __init__(self, id, username, type, password,role):
        self.username = username
        self.password = password
        self.id = id
        self.type = type
        self.role = role

    def keys(self):
        return ('id', 'username', 'password', 'type', 'role')

    def __getitem__(self, item):
        return getattr(self, item)

class Goods(db.Model):
    __tablename__ = 'goods'
    id = Column(Integer,autoincrement=True,primary_key=True)
    name = Column(String(20))
    price = Column(String(64))
    create_time =  Column(String(64))

    def __init__(self, id, name, price, create_time):
        self.id = id
        self.name = name
        self.price = price
        self.create_time = create_time


    def keys(self):
        return ('id', 'name', 'price', 'create_time')

    def __getitem__(self, item):
        return getattr(self, item)






def get_conn():
    # 建立与sql连接
    conn = sqlite3.connect('mrsoft.db')
    # c创建游标A
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):  # closed
        cursor.close()
        conn.close()


def query(sql, *args):  # query
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    conn.commit()
    close_conn(conn, cursor)
    return res

def insert_update(sql, *args):  # update
    conn, cursor = get_conn()
    res = cursor.execute(sql, args)
    conn.commit()
    close_conn(conn, cursor)
    return res

        # select * from user where username= 'yang'
def get_user(username, password):  # get user by username password
    sql = "select * from user where username= '" \
          + username \
          + "' and password= '" \
          + password \
          + "'"
    res = query(sql)
    userlist =  []
    #ajax
    for row in res:
        data = {'id': row[0], 'username': row[1], 'type': row[2], 'password': row[4], 'role': row[5]}
        userlist.append(data)
    data_dict = {"data": userlist}
    return data_dict

def get_user_by_id(id):  # get usserinfo by id
    sql = "select * from user where id=" + id
    res = query(sql)
    userlist =  []
    for row in res:
        data = {'id': row[0], 'username': row[1], 'type': row[2], 'password': row[4], 'role': row[5]}
        userlist.append(data)
    data_dict = {"data": userlist}
    return data_dict

def selectAll():  # query the use name and password
    sql = "select * from user "
    res = query(sql)
    userlist = []
    for row in res:
        data = {'id': row[0], 'username': row[1], 'type': row[2], 'password': row[4], 'role': row[5]}
        userlist.append(data)
    data_dict = {"data": userlist}
    return data_dict

def add_user(username, password):  # update user name and password
    sql = "insert into user(username,type,createtime,password,role) values('"+username+"',1,datetime(),'"+password+"','user')"
    res = insert_update(sql)
    return res

def delUserbyid(id):  # delete user name and password
    sql = "delete from user where id="+id
    res = insert_update(sql)
    return res

def update_user(id,username, password):
    sql = "updaye user set username ='"+username+"',password='"+password+"where id ="+id
    res = insert_update(sql)
    return res

def check_username(username):
    sql = "select * from user where username= '" + username + "'"
    res = query(sql)
    return res

def add_goods(name, price,typeid):
    sql = "insert into goods(name,price,create_time,typeid) values('"+name+"',"+price+",datetime(),"+typeid+")"
    print("sql:"+sql)
    res = insert_update(sql)
    return res

def buy_goods(userid,goodsid):
    sql = "insert into personal_goods_detail(userid,goodsid,create_time) values(" + userid + "," + goodsid + ",datetime())"
    print("sql:" + sql)
    res = insert_update(sql)
    return res

def add_goods_tocart(userid,goodsid):
    sql = "insert into personal_good_cart_detail(userid,goodsid,create_time) values(" + userid + "," + goodsid + ",datetime())"
    print("sql:" + sql)
    res = insert_update(sql)
    return res

def select_cart_goods_byuserid(id):
    sql = "select b.id id ,a.name name, a.price price , b.create_time create_time from goods a left join personal_good_cart_detail b  on a.id=b.goodsid where b.userid ="+id
    print("sql:" + sql)
    res = query(sql)
    print("select_cart_goods_byuserid:"+str(res))
    good = []
    if (res != None ):
        for row in res:
            data = {'id': row[0], 'name': row[1], 'price': row[2], 'create_time': row[3]}
            good.append(data)
        data_dict = {"data": good}
    else:
        data = {'id': None , 'name': None , 'price': None , 'create_time': None }
        good.append(data)
        data_dict = {"data": good}
    return data_dict

def delcart_goodsbyid(id):
    sql = "delete from personal_good_cart_detail  where id =" + id
    print(sql)
    res = insert_update(sql)
    return res


def select_purchased_goods_byuserid(id):
    sql = "select b.id id ,a.name name, a.price price , b.create_time create_time from goods a left join personal_goods_detail b  on a.id=b.goodsid where b.userid ="+id
    print("sql:" + sql)
    res = query(sql)
    print("select_purchased_goods_byuserid:"+str(res))
    good = []
    if (res != None ):
        for row in res:
            data = {'id': row[0], 'name': row[1], 'price': row[2], 'create_time': row[3]}
            good.append(data)
        data_dict = {"data": good}
    else:
        data = {'id': None , 'name': None , 'price': None , 'create_time': None }
        good.append(data)
        data_dict = {"data": good}
    return data_dict

def select_cart_goods_byuserid(id):
    sql = "select b.id id ,a.name name, a.price price , b.create_time create_time from goods a left join personal_good_cart_detail b  on a.id=b.goodsid where b.userid ="+id
    print("sql:" + sql)
    res = query(sql)
    print("select_purchased_goods_byuserid:"+str(res))
    good = []
    if (res != None ):
        for row in res:
            data = {'id': row[0], 'name': row[1], 'price': row[2], 'create_time': row[3]}
            good.append(data)
        data_dict = {"data": good}
    else:
        data = {'id': None , 'name': None , 'price': None , 'create_time': None }
        good.append(data)
        data_dict = {"data": good}
    return data_dict
def select_cart_goods_byid(id):
    sql = "select * from personal_good_cart_detail where id ="+id
    print("sql:" + sql)
    res = query(sql)
    print("personal_good_cart_detail:"+str(res))
    good = []
    if (res != None ):
        for row in res:
            data = {'id': row[0], 'userid': row[1], 'goodsid': row[2], 'create_time': row[3]}
            good.append(data)
        data_dict = {"data": good}
    else:
        data = {'id': None , 'userid': None , 'goodsid': None , 'create_time': None }
        good.append(data)
        data_dict = {"data": good}
    return data_dict

def select_cart_goods_byuuserid(id):
    sql = "select * from personal_good_cart_detail where userid ="+id
    print("sql:" + sql)
    res = query(sql)
    print("personal_good_cart_detail:"+str(res))
    good = []
    if (res != None ):
        for row in res:
            data = {'id': row[0], 'userid': row[1], 'goodsid': row[2], 'create_time': row[3]}
            good.append(data)
        data_dict = {"data": good}
    else:
        data = {'id': None , 'userid': None , 'goodsid': None , 'create_time': None }
        good.append(data)
        data_dict = {"data": good}
    return data_dict


def updateGoods(price,name,id):
    sql = "update goods set name = ' "+name+"', price = "+price+" where id =" +id
    print(sql)
    res = insert_update(sql)
    return res

def updateUsersByid(username, password, id):
        sql = "update user set username = '" + username + "', password = '" + password + "' where id =" + id
        print(sql)
        res = insert_update(sql)
        return res
    # goodslist = []
    # for row in res:
    #     data = {'id': row[0], 'name': row[1], 'price': row[2], 'create_time': row[4]}
    #     goodslist.append(data)
    # data_dict = {"data": goodslist}

def delpurachsedgoodbyid(id):
    sql = "delete from personal_goods_detail  where id =" + id
    print(sql)
    res = insert_update(sql)
    return res

def getgood(id):
    sql = "select * from goods where id= "+id
    res = query(sql)
    good =  []
    for row in res:
        data = {'id': row[0], 'name': row[1], 'price': row[2], 'create_time': row[3]}
        good.append(data)
    data_dict = {"data": good}
    return data_dict

def selectAllGoods():
    sql = "select * from goods "
    res = query(sql)
    print("sql##res:" + str(res))
    goodslist = []
    for row in res:
        data = {'id': row[0], 'name': row[1], 'price': row[2], 'create_time': row[3]}
        goodslist.append(data)
    data_dict = {"data": goodslist}
    return data_dict

def selectAllGoodsbyTypeid(id):
    sql = "select * from goods where typeid="+id
    res = query(sql)
    print("sql##res:" + str(res))
    goodslist = []
    for row in res:
        data = {'id': row[0], 'name': row[1], 'price': row[2], 'create_time': row[3]}
        goodslist.append(data)
    data_dict = {"data": goodslist}
    return data_dict

def selectbyparametr(id,typename,starttime,endtime):
    sql =" select b.id id ,a.name name, a.price price , b.create_time create_time,a.typename from (select * from goods x left join good_type y on x.typeid = y.id) a left join personal_goods_detail b  on a.id=b.goodsid  where b.userid ="+id+ \
         " and b.create_time >='"+starttime+"' and b.create_time<='"+endtime+"' and typename = '"+typename+"'"
    print("selectbyparametr sql:"+sql)
    res = query(sql)
    print("sql##res:" + str(res))
    goodslist = []
    for row in res:
        data = {'id': row[0], 'name': row[1], 'price': row[2], 'create_time': row[3],'typename':row[4]}
        goodslist.append(data)
    data_dict = {"data": goodslist}
    return data_dict




app.secret_key = 'QWERTYUIOP'  # Encrypt user information


@app.route('/login', methods=['GET', "POST"])  # post
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    userdicdata = get_user(user, pwd)
    session['user_info'] = userdicdata.get('data')
    if userdicdata.get('data')!=[]:
        print("usertype:"+str(userdicdata.get('data')))
        if(userdicdata.get('data')[0].get('type')==0):
            userlist = selectAll()
            print("userdicdata:"+str(userlist))
            return render_template('manager_personal_list.html',userlist= userlist.get('data'))
        else:
            userlist = userdicdata
            print("userdicdata:" + str(userlist))
            goodslist = select_purchased_goods_byuserid(str(userlist.get('data')[0].get('id')))
            print("goodslist:" + str(goodslist.get('data')))
            return render_template('personal_list.html', goodslist=goodslist.get('data'),userlist=userlist.get('data'),)
    else:
        return render_template('login.html', msg='用户名或密码输入错误')

@app.route('/searchPersonalgoodsListByParam')
def searchPersonalgoodsListByParam():
    # goodstype = request.args.get('goodstype')
    # starttime = request.args.get('starttime')
    # endtime = request.args.get('endtime')
    # print("searchPersonalgoodsListByParam param:"+goodstype+","+starttime+","+endtime)
    if request.args.get('goodstype') =='':
        print("goodstype is none:")
        userinfo = session['user_info'][0]
        userid = userinfo.get('id')
        print("userid:" + str(userid))
        userdicdata = get_user_by_id(str(userid))
        userlist = userdicdata
        print("returnUserPage##userdicdata:" + str(userlist))
        goodslist = select_purchased_goods_byuserid(str(userlist.get('data')[0].get('id')))
        print("goodslist:" + str(goodslist.get('data')))
        return render_template('personal_list.html', goodslist=goodslist.get('data'), userlist=userlist.get('data'))
    else:
        starttime = request.args.get('starttime')
        endtime = request.args.get('endtime')
        goodstype = request.args.get('goodstype')
        print("goodstype is not none:"+goodstype)
        if starttime =='':
            starttime = '1975-01-01 00:00:00'
        if endtime =='':
            endtime = '2099-01-01 00:00:00'
        userinfo = session['user_info'][0]
        userid = userinfo.get('id')
        print("userid:" + str(userid))
        userdicdata = get_user_by_id(str(userid))
        userlist = userdicdata
        print("returnUserPage##userdicdata:" + str(userlist))
        goodslist = selectbyparametr(str(userid),goodstype,starttime,endtime)
        print("goodslist:" + str(goodslist.get('data')))
        return render_template('personal_list.html', goodslist=goodslist.get('data'), userlist=userlist.get('data'))



@app.route('/getPersonalDetail')
def getPersonalDetail():
    id = request.args.get('id')
    print("userid:"+id)
    userdicdata = get_user_by_id(id)
    userlist = userdicdata
    print("userdicdata:" + str(userlist))
    goodslist = select_purchased_goods_byuserid(str(id))
    print("goodslist:" + str(goodslist.get('data')))
    return render_template('personal_list_bymanager.html', goodslist=goodslist.get('data'), userlist=userlist.get('data') )

@app.route('/delUser', methods=['GET', "POST"])  # post
def delUser():
    id = request.args.get('id')
    userdicdata = delUserbyid(id)
    userlist = selectAll()
    print("userdicdata:" + str(userlist))
    return render_template('manager_personal_list.html', userlist=userlist.get('data'))



@app.route('/returnManagePage')
def returnManagePage():
    userlist = selectAll()
    print("userdicdata:" + str(userlist))
    return render_template('manager_personal_list.html', userlist=userlist.get('data'))

@app.route('/returnUserPage')
def returnUserPage():
    userinfo = session['user_info'][0]
    userid = userinfo.get('id')
    print("userid:"+str(userid))
    userdicdata = get_user_by_id(str(userid))
    userlist = userdicdata
    print("returnUserPage##userdicdata:" + str(userlist))
    goodslist = select_purchased_goods_byuserid(str(userlist.get('data')[0].get('id')))
    print("goodslist:" + str(goodslist.get('data')))
    return render_template('personal_list.html',goodslist=goodslist.get('data'), userlist=userlist.get('data'))



#
# @app.route('/del')
# def del_user():
#     username = request.args.get('username')
#     mg = Manager(username)
#     msg = mg.delete()
#     return render_template('/info.html',msg=msg)

@app.route('/alluserinfo', methods=['GET', "POST"])  # post
def alluserinfo():
        request.method = 'POST'
        userlist = selectAll()
        return str(userlist.get('data'))

@app.route('/allgoodsinfo', methods=['GET', "POST"])
def allgoodsinfo():
        # request.method = 'POST'
        goodslist = selectAllGoods()
        print("goods: "+str(goodslist))
        # return str(goodslist.get('data'))
        return render_template('manage_goods_list.html',goodslist=goodslist.get('data'))

@app.route('/allgoodsinfoUser', methods=['GET', "POST"])
def allgoodsinfoUser():
        # request.method = 'POST'
        goodslist = selectAllGoods()
        print("goods: "+str(goodslist))
        # return str(goodslist.get('data'))
        return render_template('user_buy_goods_list.html',goodslist=goodslist.get('data'))

@app.route('/selectAllGoodsbyType', methods=['GET', "POST"])
def selectAllGoodsbyType():
        # request.method = 'POST'
        goodslist = selectAllGoodsbyTypeid(str(request.args.get('id')))
        print("goods: "+str(goodslist))
        # return str(goodslist.get('data'))
        return render_template('user_buy_goods_list.html',goodslist=goodslist.get('data'))


@app.route('/allcartgoodsinfoUser', methods=['GET', "POST"])
def allcartgoodsinfoUser():
        # request.method = 'POST'
        goodslist = select_cart_goods_byuserid(str(session['user_info'][0].get('id')))
        print("goods: "+str(goodslist))
        # return str(goodslist.get('data'))
        return render_template('user_cart_goods_list.html',goodslist=goodslist.get('data'))


@app.route('/getUserinfoByid', methods=['GET', "POST"])
def getUserinfoByid():
        # request.method = 'POST'
        id =  str(session['user_info'][0].get('id'))
        userlist = get_user_by_id(id)
        print("userlist: "+str(userlist))
        # return str(goodslist.get('data'))
        return render_template('user_info_edit.html',userlist=userlist.get('data'))

@app.route('/updategood', methods=['GET', "POST"])
def updategoodinfo():
    name = request.args.get('name')
    price = request.args.get('price')
    id = request.args.get('id')
    print("updategood name price id:"+str(name)+" "+str(id)+" "+str(price))
    res  = updateGoods(price,name,id)
    if(res):
        goodslist = selectAllGoods()
        print("goods: " + str(goodslist))
        return render_template('manage_goods_list.html',goodslist=goodslist.get('data'))
    else:
        return render_template('goodinfo.html', msg='update failed')

@app.route('/updateuserbyid', methods=['GET', "POST"])
def updateuserbyid():
    username = request.args.get('username')
    password = request.args.get('password')
    id = request.args.get('id')
    print("username name password id:"+str(username)+" "+str(id)+" "+str(password))
    res  = updateUsersByid(username,password,id)
    userlist = get_user_by_id(id)
    print("userlist: " + str(userlist))
    if(res):
        # return str(goodslist.get('data'))
        return render_template('user_info_edit.html',userlist=userlist.get('data'),msg='update successful')
    else:
        return render_template('user_info_edit.html',userlist=userlist.get('data'), msg='update failed')

@app.route('/getgood', methods=['GET', "POST"])
def getgoodinfo():
        id = request.args.get('id')
        print('id: '+id)
        goodslist = getgood(id)
        # return str(goodslist.get('data'))
        return render_template('goodinfo.html',goodslist=goodslist.get('data'))

@app.route('/buygood', methods=['GET', "POST"])
def buygood():
        userinfo = session['user_info'][0]
        userid = str(userinfo.get('id'))
        goodsid = request.args.get('id')
        res = buy_goods(userid, goodsid)

        if(res):
            goodslist = selectAllGoods()
            print("goods: " + str(goodslist))
            return render_template('user_buy_goods_list.html', goodslist=goodslist.get('data'), msg='sucess')
        else:
            goodslist = selectAllGoods()
            print("goods: " + str(goodslist))
            return render_template('user_buy_goods_list.html', msg='plz try again')

@app.route('/buygoodfromcart', methods=['GET', "POST"])
def buygoodfromcart():
        userinfo = session['user_info'][0]
        userid = str(userinfo.get('id'))
        id = request.args.get('id')

        goodsid =  str( select_cart_goods_byid(id).get('data')[0].get('goodsid'))
        res = buy_goods(userid, goodsid)
        delcart_goodsbyid(id)

        if(res):
            goodslist = select_cart_goods_byuserid(userid)
            print("goods: " + str(goodslist))
            return render_template('user_cart_goods_list.html', goodslist=goodslist.get('data'), msg='sucess')
        else:
            goodslist = select_cart_goods_byuserid(userid)
            print("goods: " + str(goodslist))
            return render_template('user_cart_goods_list.html', msg='plz try again')

@app.route('/buyAllgoodfromcart', methods=['GET', "POST"])
def buyAllgoodfromcart():
        userinfo = session['user_info'][0]
        userid = str(userinfo.get('id'))
        id = request.args.get('id')

        goodlist =  select_cart_goods_byuuserid(userid).get('data')
        print("buyAllgoodfromcart goodlist:"+str(goodlist))
        for i in range(len(goodlist)):

           goodsid = str(goodlist[i].get('goodsid'))
           res = buy_goods(userid, goodsid)
           delcart_goodsbyid(str(goodlist[i].get('id')))
        if(res):
            goodslist = select_cart_goods_byuserid(userid)
            print("goods: " + str(goodslist))
            return render_template('user_cart_goods_list.html', goodslist=goodslist.get('data'), msg='sucess')
        else:
            goodslist = select_cart_goods_byuserid(userid)
            print("goods: " + str(goodslist))
            return render_template('user_cart_goods_list.html', msg='plz try again')


@app.route('/addtocart', methods=['GET', "POST"])
def addtocart():
        userinfo = session['user_info'][0]
        userid = str(userinfo.get('id'))
        goodsid = str(request.args.get('id'))
        res = add_goods_tocart(userid, goodsid)

        if(res):
            goodslist = selectAllGoods()
            print("goods: " + str(goodslist))
            return render_template('user_buy_goods_list.html', goodslist=goodslist.get('data'), msg='sucess')
        else:
            goodslist = selectAllGoods()
            print("goods: " + str(goodslist))
            return render_template('user_buy_goods_list.html', msg='plz try again')


@app.route('/delpurachsedgood', methods=['GET', "POST"])
def delpurachsedgood():
        goodsid = request.args.get('id')
        print("delpurachsedgood id:"+str(goodsid))
        res = delpurachsedgoodbyid(goodsid)
        userdicdata = get_user_by_id(str(session['user_info'][0].get('id')))
        userlist = userdicdata
        print("userdicdata:" + str(userlist))
        goodslist = select_purchased_goods_byuserid(str(userlist.get('data')[0].get('id')))
        print("goodslist:" + str(goodslist.get('data')))
        return render_template('personal_list.html', goodslist=goodslist.get('data'), userlist=userlist.get('data'), )

@app.route('/movefromcart', methods=['GET', "POST"])
def movefromcart():
        goodsid = request.args.get('id')
        print("delpurachsedgood id:"+str(goodsid))
        res = delcart_goodsbyid(str(goodsid))
        # userdicdata = get_user_by_id(str(session['user_info'][0].get('id')))
        # userlist = userdicdata
        # print("userdicdata:" + str(userlist))
        goodslist = select_cart_goods_byuserid(str(session['user_info'][0].get('id')))
        print("goodslist:" + str(goodslist.get('data')))
        return render_template('user_cart_goods_list.html', goodslist=goodslist.get('data') )




@app.route('/addgood', methods=['GET', "POST"])
def addgood():
        name = request.args.get('name')
        price = request.args.get('price')
        typeid = request.args.get('typeid')
        res = add_goods(name, price,typeid)

        if(res):
            goodslist = selectAllGoods()
            print("goods: " + str(goodslist))
            return render_template('manage_goods_list.html', goodslist=goodslist.get('data'), msg='sucess')
        else:
            goodslist = selectAllGoods()
            print("goods: " + str(goodslist))
            return render_template('manage_goods_list.html', msg='plz try again')


@app.route('/index')
def index():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    return 'hello'

@app.route('/register', methods=['GET', "POST"])
def register():
    if request.method == 'POST':
         user = request.form.get('username')
         pwd = request.form.get('password')
         # check the name exist
         check_res = check_username(user)
         if check_res:
             return flash('username already exist!')
         else:
             res = add_user(user, pwd)
             print("user:" + user + " pwd:" + pwd + " res:" + str(res))
             pwd2 = request.form.get('password2')
             if not all([user, pwd, res]):
                flash('参数不完整')
             elif pwd != pwd2:
                flash('两次密码不一致，请重新输入')
             else:
                new_user = Users(username=user, password=pwd, id=None,type=1,role='user')
                session['user_info'] = user
                return redirect('/login')
    return render_template('register.html')



@app.route('/logout')
def logout_():
    del session['user_info']
    return redirect('login')


if __name__ == "__main__":
    app.run()






