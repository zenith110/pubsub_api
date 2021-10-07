# import pillow


def resize_image(sub_image):
    pass


def check_image(sub_name, original_image, my_bucket, pubsub):
    sub_name = sub_name.lower().replace(" ", "-")
    try:
        """
        Retrives the images from AWS S3
        """
        for object_summary in my_bucket.objects.filter(
            Prefix=sub_name
        ):
            if(object_summary.key == sub_name + ".jpg"):
                pubsub.image.append("https://pubsub-images.s3.us-east-2.amazonaws.com/"
                                    + object_summary.key)

    except Exception as error:
        print(error)
    return pubsub
