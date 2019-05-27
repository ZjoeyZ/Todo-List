# A Todo_List on web  

1，使用我的[simple-client-and-server](https://github.com/ZjoeyZ/simple-client-and-sever)仓库中的sever4框架，结合sever5中的内容实现用户登录  
2，再实现一个简单的Todo-List 应用，能够让用户增删改查  
3，将这个应用和用户结合，让每个用户拥有自己的Todo-List

# 在sever框架基础上实现用户注册、登录和验证
1，补充request对象，让解析是能得到请求里的headers字段，和cookie  
2, 实现用户登录功能，
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
                
# 在sever框架基础上实现Todo_list应用         
1, 实现todo_list功能，
   - M:Todo对象的实现 
        1. title属性存储信息
        2. id属性唯一表示符,初始值能get就get，get不到就保存为-1
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
        
# 将Todo_list应用和用户联系起来，让每个用户只能对自己的todo-list进行操作 
   - 给User对象增加id属性，user注册时会分配id，用户登录时分配的session_id和id对应
   - Todo对象的增加user_id属性，
   - 所以要让用户先登录，在使用todo_list，没登录返回重定位
   -    要add todo时会更根据用户信息，给todo增加user_id属性
   -    让todo页面只显示属于用户的todo
   -    让用户只能编辑属于自己的todo

# 小BUG
   - 刚启动服务器的第一个登陆用户要登陆两次才能进入todo_list

# 将模板更新成jinjia实现  
   - 将模板用jinjia语法写
   - 用更新各个返回模板的函数
