# A Todo_List on web  

1，使用我的[simple-client-and-server](https://github.com/ZjoeyZ/simple-client-and-sever)仓库中的sever4框架，结合sever5中的内容实现用户登录  
2，再实现一个简单的Todo-List 应用，能够让用户增删改查  
3，将这个应用和用户结合，让每个用户拥有自己的Todo-List

# 开始
一，首先复制sever4框架，然后准备添加用户功能  
1，补充request对象，让解析是能得到请求里的headers字段，和cookie  
2, 实现用户登录功能，
    M:User对象的实现 
    V:register.html login.html的实现
    C:route_index route_register函数的实现  
        route_register：1，如果不是post请求返回一个登录页面response
                        2，如果是post请求，根据请求表单，生成对象，并保存
                        返回一个登录成功的页面  
        route_register：1，非post返回登录页面
                        2，post，生成对象，验证对象：
                            若检验成功
                            生成session，与用户信息建立联系（加入字典）
                            在要返回的headers字段里增加set-cookie字段，加入session



