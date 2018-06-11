from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Post
from .models import Comment
from .forms import CommentForm

"""这里开始变得复杂了，我需要写大量注释才好"""


def post_comment(request, post_pk):
    """
    这里使用了 post.comment_set.all() 来获取 post 对应的全部评论。
    Comment 和Post 是通过 ForeignKey 关联的，回顾一下我们当初获取某个分类 cate 下的全部文章时的代码：
    Post.objects.filter(category=cate)。这里 post.comment_set.all() 也等价于 Comment.objects.filter(post=post)，
    即根据 post 来过滤该 post 下的全部评论。但既然我们已经有了一个 Post 模型的实例 post（它对应的是 Post 在数据库中的一条记录），
    那么获取和 post 关联的评论列表有一个简单方法，即调用它的 xxx_set 属性来获取一个类似于 objects 的模型管理器，
    然后调用其 all 方法来返回这个 post 关联的全部评论。 其中 xxx_set 中的 xxx 为关联模型的类名（小写）。
    例如 Post.objects.filter(category=cate) 也可以等价写为 cate.post_set.all()。
    """
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。

        if form.is_valid():
            comment = form.save(commit=False)
            # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment.post = post
            comment.save()
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list,
            }
            return render(request, 'blog/detail.html', context=context)
    # 若不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    # redirect 既可以接收一个URL作为参数，也可以接收一个模型的实例作为参数（例如这里的post）。
    # 如果接收一个模型的实例，那么这个实例必须实现了get_absolute_url方法，
    # 这样 redirect 会根据 get_absolute_url 方法返回的URL值进行重定向。
    return redirect(post)
