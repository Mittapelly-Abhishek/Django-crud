from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . models import usertable
from . serializers import userserializer
import json
import cloudinary
import cloudinary.uploader
# Create your views here.

@csrf_exempt 
def reg_user(req):
    if req.method=="POST":
        try:
            id=req.POST.get("user_id")
            name=req.POST.get("user_name")
            email=req.POST.get("user_email")
            password=req.POST.get("user_password")
            image=req.FILES.get("user_image")

            img_url=cloudinary.uploader.upload(image)

            new_user=usertable.objects.create(user_id=id,user_name=name,user_email=email,user_password=password,user_image=img_url["secure_url"])

            return JsonResponse({"msg":"user created successfully"})
        
        except Exception as e:
            return JsonResponse({"error":str(e)},status=400)
        
    return JsonResponse({"error":"only POST methods is available"})


def get_user(req,id):
    if req.method=="GET":
        try:
            single_user=usertable.objects.get(user_id=id)
            serializer=userserializer(single_user)
            return JsonResponse(serializer.data,safe=False)
        
        except usertable.DoesNotExist:
            return JsonResponse({"error":"user not found"},status=404)

    return JsonResponse({"error":"only get method is allowed"})

def get_users(req):
    users_data=usertable.objects.all()
    serializers=userserializer(users_data,many=True)
    return JsonResponse({"users_data":serializers.data})


@csrf_exempt
def update_user(req,id):
    if req.method=="PUT":
        try:
            single_user=usertable.objects.get(user_id=id)
        except usertable.DoesNotExist:
            return HttpResponse("user not found",status=404)
    
        user_data=json.loads(req.body)
        serailizer=userserializer(single_user,data=user_data)

        if serailizer.is_valid():
            serailizer.save()
            return HttpResponse("user updated succfully",status=200)
        return JsonResponse(serailizer.errors,status=400)
    
    else:
        return HttpResponse("only put method is allowed")
    
@csrf_exempt
def patch_user(req,id):
    if req.method=="PATCH":
        try:
            single_user=usertable.objects.get(user_id=id)
        except usertable.DoesNotExist:
            return HttpResponse("user not found",status=404)
    
        user_data=json.loads(req.body)
        serailizer=userserializer(single_user,data=user_data,partial=True)

        if serailizer.is_valid():
            serailizer.save()
            return HttpResponse("user updated succfully",status=200)
        return JsonResponse(serailizer.errors,status=400)
    
    else:
        return HttpResponse("only patch method is allowed")



@csrf_exempt   
def delete_user(req,id):
    if req.method=="DELETE":
        
        try:
            emp=usertable.objects.get(user_id=id)
        except usertable.DoesNotExist:
            return HttpResponse("user not found",status=404)
        emp.delete()
        return HttpResponse("user deleted successfully",status=204)
    else:
        return HttpResponse("only delete method is allowed")




        
        
