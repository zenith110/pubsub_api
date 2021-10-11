import requests
from PIL import Image
from io import BytesIO


def resize_image(sub_image):
    sub_image.thumbnail((360, 360))
    img_byte_arr = BytesIO()
    sub_image.save(img_byte_arr, format="JPEG")
    return img_byte_arr.getvalue()


def upload_image(sub_download_link, my_bucket, sub_name):
    sub_image_request = requests.get(sub_download_link)
    image = Image.open(BytesIO(sub_image_request.content))
    if(image.size == (360, 360)):
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format="JPEG")
        my_bucket.put_object(Key=sub_name + ".jpg",
                             Body=img_byte_arr.getvalue(), ContentType="image/jpeg", ACL="public-read")
    else:
        resized_pubsub_image = resize_image(image)
        my_bucket.put_object(Key=sub_name + ".jpg",
                             Body=resized_pubsub_image, ContentType="image/jpeg", ACL="public-read")


def check_image(sub_name, original_image, my_bucket, pubsub):
    sub_found = False
    sub_name = sub_name.lower().replace(" ", "-")
    """
    Retrives the images from AWS S3
    """
    for object_summary in my_bucket.objects.filter(
        Prefix=sub_name
    ):
        if(object_summary.key == sub_name + ".jpg"):
            sub_found = True
            pubsub.image.append("https://pubsub-images.s3.us-east-2.amazonaws.com/"
                                + object_summary.key)
        else:
            sub_found = False
            continue
    if(sub_found is False):
        upload_image(original_image, my_bucket, sub_name)
    return pubsub
