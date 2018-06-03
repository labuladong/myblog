# myblog

我的blog项目，首页地址[在这里](http://39.108.239.113/)

功能正在完善，但是基本的app逻辑，数据库表单已经完善，对大型网站的建设有实践意义。下面我来分享一下我这次实践中对web开发的一点理解。

## 整体概述

个人博客实际上只相当于网站结构上的一个app，而真正的网站肯定需要不止一个app，但是 **总体流程是不会变的**：

### app逻辑设计 

首先要明确网站 *要做什么* 。比如这个博客系统，功能主要有二，第一是博主后台发文，第二是浏览者评论。那么具体功能呢？

- 首先文章需要有作者，正文，标题，创建时间，这样就行了吗？ **太简陋**，稍微好点的文章管理系统至少还得有个文章分类功能吧（[Category](https://github.com/fudonglai/myblog/blob/master/blog/models.py)）例如技术文章可以分为 Java，Python 等等 Categories，而且点击分类会跳转到相应的分类下所有文章的页面。

- 但是当文章数据库庞大之后简单的categories可能不能满足用户需求，比如说用户在 Python 分类下看到一篇 Django 教程，感觉不错，还想再找一篇类似的博文看看。但是由于Python 标签下文章太多，只能通过全局搜索来找，这就显得很麻烦用户。所以可以新增一个文章标签功能 [Tag](https://github.com/fudonglai/myblog/blob/master/blog/models.py)，就是说在刚才用户看的那篇 Django 教程应该有这样几个标签：*Python*, *Django*, *web 开发*, *后端* 等等。

- 现在说说浏览者评论，这是 blog 项目中必要的功能，怎么做？请详述实现需求。首先评论区应该在每篇 blog 的详情界面，而且应该在最底部，看看 *百度知道* 每次把用户回答框放在页面最上方我也是醉了。然后，用户评论需要提供哪些信息，那些是必须的，那些是非必需的？参见我这个blog的 [Detail界面](http://39.108.239.113/post/7/)，你可以试试，我是把 URL 信息设为非必需选项，其他都是必须填写的。

### 数据库模型设计

网站和网页最大的不同就是：网页只是一个公告栏，只需要实现简单的跳转，无法实现更多功能（例如账号登陆，服务器与用户交互等）；而网站的后台本质上是一个框架驱动的程序，能够持久化关键数据，通过网页的包装，能够为用户提供更完善的功能。网站正常运行除了后台框架的中间件和引擎之外，最重要的就是数据库。

以这个博客为例，我来分析一下简单的文章系统和评论系统的数据模型。

- 明确app逻辑后，需要进行[**模型 models 文件**](https://github.com/fudonglai/myblog/blob/master/blog/models.py) 编写，model指的是 *数据关系* 模型，也就是设计数据库。例如我的这个博客的数据库模型[在这里](https://github.com/fudonglai/info_sys_python/blob/master/Django_code_comments/db.sqlite3)，其中的SQL代码是python自动生成的，但是数据库逻辑和优化必须要这方面的朋友来做。

- 我的blog项目里面其实包含了两个 app，一个是文章相关的信息，请看 [Post 模型](https://github.com/fudonglai/myblog/blob/master/blog/models.py)，共包含9个属性：*title*, *author*, *created_time*, *modfied_time*, *body*, *category*, *tag*, *excerpt*, *views(访问量)* 。一个是评论相关信息，请看[Comment模型](https://github.com/fudonglai/myblog/blob/master/comments/models.py), 包含 *name，email，url，text created_time，post* 属性，其中 post 作为 Post 模型的外键。

- Django 建议将评论和文章分开，两个关系只需要一个外键连接就好。对于这么多属性，我也学着做了一下优化：最主要的是文章信息，由于数据冗余的问题，我把表单分成了两个，具体请看[数据库模型](https://github.com/fudonglai/info_sys_python/blob/master/Django_code_comments/db.sqlite3)。其中包含一对多的 ForeignKey 关系（Category对Post，Author对Post），多对多关系（Tag和Post），需要明确的是一对多关系的删除异常问题，我就忽略这个问题，导致删除某个 Category 导致所有文章删除。我现在似乎还没解决这个问题，数据库方向的同学可以帮我我检查优化一下，我来修改。

### 视图逻辑

视图逻辑编写，即[ views 文件和 urls 映射 ](https://github.com/fudonglai/myblog/tree/master/blog)。比如你可以观察我的博客中不同功能区的url特点，不同功能区需要明确的url区分，然后对应到[templates](https://github.com/fudonglai/myblog/tree/master/blog/templates)中相应的HTML文件显示视图。

这里就是后端需要做的事了，具体不用多说。
  
### 网页制作

制作css样式和js渲染，属于前端，这个我不了解，我的css和js是[网上下载的模板](https://github.com/zmrenwu/django-blog-tutorial-templates)，觉得我这个模板好看的朋友可以去研究研究。

HTML文件要尽量 **便于后端改造** 成[Django渲染模板](https://github.com/fudonglai/myblog/tree/master/blog/templates)(注意html中有很多{%  %} {{  }}这样的标记，这就是 Django 的HTML上下文映射)。

 ## 个人体会
  
  体验了一波web开发，感受很深，一路从后端开发到前端实现再到云端部署，真的学到了很多，虽然将来不会去做web开发，但也是给自己积累了这方面经验，何况还做出一个像模像样的博客系统，也是对自己学习能力的肯定吧。
  
  网络上类似的教程很多，我这里就不贴网址了，想要学的同学还是找合适自己的教程跟着学一下就好。但我的建议是先把[官方文档看完](https://docs.djangoproject.com/zh-hans/2.0/intro/)，我的学习方法是边看教程边敲代码边写注释，我的学习代码在[这里](https://github.com/fudonglai/info_sys_python/tree/master/Django_code_comments)，可以参照一下我的代码注释，我把所有踩到坑都记录了，这帮助我加速了之后的学习。
  
  另外我体会颇深的一点是，像这样一个简单的博客系统（因为严格来说他只有一个应用）都包含如此复杂的结构，即便用了最强大的框架，它的制作也让我大费周折：w网站开发确实是一项团队的任务，Django 倡导前后端分离，我的水平暂时也就能维护这样一个简单的网站系统了，而对我一个人而言，我也算是达成了一个目标。个人开发的优势在于对各方面的情况了解透彻，即便堆栈跟踪出现数十行错误也能理出问题所在；这也就是近年来流行“全栈工程师”的原因吧。
  
  最后，这个博客我暂时应该不会再去维护和改良了，但是会偶尔发些文章，假期再进行进一步测试和改良。以后我会把这个博客作为一个平台，输出一些自认为有价值的东西，培养写作能力。欢迎关注我的博客。有兴趣的朋友应该亲自动手去做自己擅长的方面，“用以致学”，多维度配技术合才能实现更大目标。
  
  
