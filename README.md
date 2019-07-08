# A Todo_List on web 
一个不断迭代中的web应用，使用我的[simple-client-and-server](https://github.com/ZjoeyZ/simple-client-and-sever)仓库中的sever4框架  
目前功能：
  
    - 用户注册和登录  
    - 每个用户可使用自己的Todo-List 应用，能够让每个用户增删改查  
    - 使用jinjia模板、密文存储用户密码

# 1、用户注册、登录和验证
1，完善request对象，让解析是能得到请求里的headers字段，和cookies  
2，实现用户登录功能，
   - M:User对象的实现 
   - V:register.html login.html的实现
   - C:route_index route_register函数的实现
     
        - route_register：
            1. 如果不是post请求返回一个登录页面response
            2. 如果是post请求，根据请求表单，生成对象，并保存
               返回一个登录成功的页面 
                         
        - route_login:
            1. 非post返回登录页面
            2. post，生成对象，验证对象，若检验成功，  
            生成session，与用户名称建立联系
                返回set-cookie字段
                返回登录成功页面
                
# 2、Todo_list应用         
   - M:Todo对象的实现 
        - title属性存储信息
        - id属性唯一表示符,初始值能get就get，get不到就保存为-1
          最开始是直接赋值为-1后来出现bug：load出来的对象实例化也都直接赋值为1了
          需要在保存时，给Todo实列赋值一个唯一id
        
   - V:todo.html todo_update.html的实现
       - todo.html：
            1. 显示todo_list页面
            2. 发送post请求，到/todo/add根据请求表单，请求添加todo
            3. 发送get请求，到/todo/delete根据query ?id=，请求删除指定todo
            4. 发送get请求，到/todo/edit，根据query ？id=，返回修改页面
            
       - todo_update.html    
            1. 显示修改页面
            2. 发送post请求到，todo/update,根据请求处理数据，返回重定位
                          
   - C:route_todo route_add_todo route_delete_todo route_update_todo函数的实现   
        - route_todo：
            1. 返回一个todo_list页面
                         
        - route_add_todo:
            1. 根据POST请求表单，添加todo，并保存
               返回一个重定位到/todo的response
               
        - route_delete_todo:
            1. 根据GET请求query，删除指定todo，并保存
               返回一个重定位到/todo的response
        
        - route_edit_todo:
            1. 根据GET请求query，显示页面
            
        - route_edit_todo:    
            1. 根据POST请求，删除指定todo，并保存
               返回一个重定位到/todo的response
        
# 3、每个用户只能对自己的todo-list进行操作 
   - 给User对象增加id属性，user注册时会分配id，用户登录时分配的session_id和id对应
   - Todo对象的增加user_id属性，
   - 所以要让用户先登录，在使用todo_list，没登录返回重定位
   -    要add todo时会更根据用户信息，给todo增加user_id属性
   -    让todo页面只显示属于用户的todo
   -    让用户只能编辑属于自己的todo

# 小BUG
   - 刚启动服务器的第一个登陆用户要登陆两次才能进入todo_list
   - 解决：问题原因：用户端及时set了cookies，
                   服务器应该根据新cookie统一访问\todo
                   但还是没有，说明cookie没有及时更新
                   后来发现cookie更新的函数果然在发送response之后
                   
# 5、将模板更新成jinjia实现  
   - 将模板用jinjia语法写
   - 用更新各个返回模板的函数
   
# 6、使用密文存储用户密码
   - 修改user的注册路由函数，在注册时将密码转成密文
   - 修改user的exist函数，检验时也要将明文密码转密文密码
   - 密文加盐在加密做为密码存储
   
# 7、使用数据库存储数据
   - 之前的增删查改每次都是load和save所有的数据
   - 现在为每个对象的增删查改创建函数，对sqlite数据库进行操作
   - 第一步：
            更新用户注册
            覆盖了User的父类save方法，用sql insert的方式重写
            todo：应该让用户名具有唯一性
   - 第二步：
            更新用户登录
                找到原来用户登录的route-修改的exist()-修改user.all()
                之前都是通过在所有对象里遍历查找，现在可以用sql语句直接查找
                问题：
                    username数据库格式是interger，已修改
                    routes里验证问user存在只有不需要重新find user，直接用它就行
            更新todo
                1, 创建todo表
                2, 修改todo.all
                    修改todo.all 利用sql select * 结合u_id得到todo
                    修改jinjia，因为传入的不是todo对象，而是todo tuple
                3, 修改
                    增：重写了todo.save
                    删：根据id, user_id创建对象
                        p判断对象是否存在与数据库
                        有则删除
                        重定位
                    改
                    查
