from django.shortcuts import render
from app.models import Content, Channel, ContentDetails
import redis

redis_client = redis.Redis(host="redis", port=6379, db=0)


def index(request):
    contentRating = calculateRating()
    context = {
        "contents": Content.objects.filter(is_active=True),
        "channels": Channel.objects.all(),
        "contentRating": contentRating
    }
    return render(request, "app/index.html", context)


def contents_by_chanel(request, slug):
    contentRating = calculateRating()
    contents = Content.objects.filter(is_active=True, channel__slug=slug)
    context = {
        "contents": contents,
        "channels": Channel.objects.all(),
        "selected_channel": slug,
        "contentRating": contentRating
    }

    return render(request, "app/contents.html", context)


def content_details(request, slug):
    contents = ContentDetails.objects.filter(cont__slug=slug)
    context = {
        "contents": contents,
        "channels": Channel.objects.all()
    }

    return render(request, "app/content-details.html", context)


def detail(request, slug):
    content = ContentDetails.objects.get(slug=slug)
    user_already_voted = redis_client.get("{}_{}".format(request.user.username, content.id))
    content_already_set = redis_client.get(str(content.id))

    if content_already_set is not None:
        voteRating = float(int(redis_client.get(str(content.id)))
                           / int(redis_client.get(str(content.id) + "_")))
    else:
        voteRating = 0

    if user_already_voted is not None:
        voted = True
    else:
        voted = False

    if request.user.is_authenticated:
        if request.method == "POST":
            rating = request.POST.get("rating")
            if user_already_voted is not None:
                voted = True
            else:
                if content_already_set is not None:
                    if user_already_voted is not None:
                        redis_client.incr(str(content.id), rating)
                        redis_client.incr(str(content.id) + "_", 1)
                    else:
                        redis_client.incr(str(content.id), rating)
                        redis_client.incr(str(content.id) + "_", 1)
                        redis_client.set("{}_{}".format(request.user.username, content.id), 1)
                else:
                    redis_client.set(str(content.id), rating)
                    redis_client.set(str(content.id) + "_", 1)
                    redis_client.set("{}_{}".format(request.user.username, content.id), 1)

                voted = True
                voteRating = float(int(redis_client.get(str(content.id)))
                                   / int(redis_client.get(str(content.id) + "_")))
                context = {
                    "content": content,
                    "channels": Channel.objects.all(),
                    "vote": "Rating:{}/5".format(str(round(voteRating, 2))),
                    "voted": voted
                }
                return render(request, "app/details.html", context)
        else:
            if user_already_voted is not None:
                voted = True
            context = {
                "content": content,
                "channels": Channel.objects.all(),
                "vote": "Rating:{}/5".format(str(round(voteRating, 2))),
                "voted": voted
            }
            return render(request, "app/details.html", context)
    context = {
        "content": content,
        "channels": Channel.objects.all(),
        "vote": "Rating:{}/5".format(str(round(voteRating, 2))),
        "voted": voted
    }
    return render(request, "app/details.html", context)


def calculateRating():
    contents = ContentDetails.objects.all()

    new = []
    for content in contents:
        totalRating = 0
        numberRating = 0
        if redis_client.get(str(content.id)) is not None:
            totalRating += int(redis_client.get(str(content.id)))
            numberRating += int(redis_client.get(str(content.id) + "_"))
        new.append([content.cont.title, totalRating, numberRating])

    output_dict = {}
    for key, *values in new:
        if key not in output_dict:
            output_dict[key] = [values]
        else:
            output_dict[key] = output_dict[key]
            output_dict[key][0][0] += values[0]
            output_dict[key][0][1] += values[1]

    result = []
    for i in output_dict:
        if output_dict[i][0][0] is not 0:
            result.append((i, float(output_dict[i][0][0] / output_dict[i][0][1])))

    return result
