from django.shortcuts import render ,get_object_or_404
from django.utils import timezone
from .models import childinfo, userdata,typecci,cci,lostchild,parent,doner,Post ,Comment,cases
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from .forms import LostForm ,ChildForm,ParentForm,DonorForm,PostForm,CommentForm,CaseForm






@login_required
def homepage(request):
	return render(request,"child/homepage.html")

def institute(request):
	ins=typecci.objects.all()
	return render(request,"child/institution.html",{"ins":ins})

@login_required
def special(request):
	info=cci.objects.filter(typ__name__contains="Special Homes")
	return render(request,"child/special.html",{'info':info})
@login_required
def childlistdl(request):
	info=childinfo.objects.filter(State__contains="Delhi")
	return render(request,"child/delhi.html",{'info':info})


@login_required
def children(request):
		info=cci.objects.filter(typ__name__contains="Children Home",)
		return render(request,"child/children.html",{'info':info})
@login_required
def childlistjp(request):
	info=childinfo.objects.filter(State__contains="Jaipur")
	return render(request,"child/jaipur.html",{'info':info})

@login_required
def place(request):
		info=cci.objects.filter(typ__name__contains="Place")
		return render(request,"child/place.html",{'info':info})
@login_required
def childlistmb(request):
	info=childinfo.objects.filter(State__contains="Mumbai")
	return render(request,"child/mumbai.html",{'info':info})
@login_required
def observation(request):
		info=cci.objects.filter(typ__name__contains="Observation Home",)
		return render(request,"child/observation.html",{'info':info})
@login_required
def childlistkl(request):
	info=childinfo.objects.filter(State__contains="Kolkata")
	return render(request,"child/kolkata.html",{'info':info})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'child/signup.html', {'form': form})




@login_required
def lost(request):
	info=lostchild.objects.all()
	return render(request,"child/lost.html",{'info':info})


@login_required
def addlost(request):
	if request.method == "POST":
		form = LostForm(request.POST)
		if form.is_valid():
			child = form.save(commit=False)
			child.save()
			return redirect('lost')
	else:
		form = LostForm()
	return render(request, 'child/addlost.html', {'form': form})




@login_required
def addchild(request):
	if request.method == "POST":
		form = ChildForm(request.POST)
		if form.is_valid():
			child = form.save(commit=False)
			child.save()
			return redirect('institute')
	else:
		form = ChildForm()
	return render(request, 'child/addchild.html', {'form': form})

@login_required
def adoptionlist(request):
	info=childinfo.objects.all()
	return render(request,'child/adoptionlist.html',{'info':info})

@login_required
def parentform(request):
	if request.method == "POST":
		form = ParentForm(request.POST)
		if form.is_valid():
			child = form.save(commit=False)
			child.save()
			return redirect('adoptionlist')
	else:
		form = ParentForm()
	return render(request, 'child/parentform.html', {'form': form})



@login_required
def donorform(request):
	if request.method == "POST":
		form = DonorForm(request.POST)
		if form.is_valid():
			donor = form.save(commit=False)
			donor.save()
			return redirect('homepage')
	else:
		form = DonorForm()
	return render(request, 'child/donorform.html', {'form': form})





@login_required
def post_list(request):
	posts=Post.objects.all()
	if request.method == "POST":
		form = CaseForm(request.POST)
		if form.is_valid():
			case = form.save(commit=False)
			case.save()
			return redirect('post_list')
	else:
		form = CaseForm()
	return render(request, 'child/post_list.html', {'form': form})
	
	return render(request,"child/post_list.html",{'posts':posts})


def post_detail(request, pk):
    
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'child/post_detail.html', {'post': post})



@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'child/post_edit.html', {'form': form})









def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'child/post_edit.html', {'form': form})



@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')



@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'child/add_comment_to_post.html', {'form': form})



@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)



@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)



@login_required
def index(request):
    latest_question=Question.objects.order_by("-pub_date")[:5]
    
    context={"latest_question":latest_question}
    return render(request,"child/index.html",context)



@login_required
def detail(request,pk):
    
    question=get_object_or_404(Question,pk=pk)
    
    return render(request,"blog/detail.html",{"question":question})




def caseform(request):
	if request.method == "POST":
		form = CaseForm(request.POST)
		if form.is_valid():
			case = form.save(commit=False)
			case.save()
			return redirect('post_list')
	else:
		form = CaseForm()
	return render(request, 'child/post_list.html', {'form': form})





