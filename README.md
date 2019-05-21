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
3, 实现todo_list功能，
   - M:*Todo对象的实现 
        
   - V:*todo.html todo_edit.html的实现
       - todo.html：
            1. 显示todo_list页面
            2. 发送post请求，到/todo/add根据请求表单，请求添加todo
                         
   - C:*route_todo route_add_todo route_delete_todo route_edit_todo函数的实现   
        - route_todo：
            1. 返回一个todo_list页面
                         
        - route_add_todo:
            2. 根据请求表单，添加todo，并保存
               返回一个重定位到/todo的response


