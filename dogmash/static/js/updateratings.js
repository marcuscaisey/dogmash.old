const fadeDuration = 300;
const transitionDuration = 500;

$(document).ready(function () {
    $("img.dog").click(function () {
        let winnerId = parseInt($(this).attr("id"));
        let loserId;

        for (let img of $("img.dog")) {
            let id = parseInt(img.id);
            if (id != winnerId) {
                loserId = id;
            }
        }

        $.post("updateratings", {
            "winner_id": winnerId,
            "loser_id": loserId,
        }, function (data) {
            $(`#rank${winnerId}`).text(data["winner"]["rank"]);
            $(`#rating${winnerId}`).text(data["winner"]["rating"]);
            $(`#rank${loserId}`).text(data["loser"]["rank"]);
            $(`#rating${loserId}`).text(data["loser"]["rating"]);

            $(`#rank-change${winnerId}`).text(`(${data["winner"]["rank_change"]})`).addClass("winner");
            $(`#rating-change${winnerId}`).text(`(${data["winner"]["rating_change"]})`).addClass("winner");
            $(`#rank-change${loserId}`).text(`(${data["loser"]["rank_change"]})`).addClass("loser");
            $(`#rating-change${loserId}`).text(`(${data["loser"]["rating_change"]})`).addClass("loser");

            // Fix position of ranks/ratings so they don't get re-centred.
            $(".rank-container, .rating-container").each(function () {
                $(this).css({
                    "position": "relative",
                    "left": $(this).position().left - 1,
                });
                $(this).parent().css("text-align", "initial");
            });

            // Fix width/height of table fields so that their contents remain
            // fixed whilst other contents are faded in and out.
            $("#dog-table td").each(function () {
                $(this).css({
                    "width": $(this).width(),
                    "height": $(this).height(),
                });
            });

            $(".change").fadeIn(fadeDuration).promise().done(function () {
                setTimeout(function () {
                    // Need to wait for images to load until fading all
                    // elements in, so that they fade in at the same time.
                    $("img.dog").on("load", function () {
                        $(this).fadeIn(fadeDuration);
                        $(".rank, .rating").fadeIn(fadeDuration);
                        $("*").removeAttr("style");
                    });

                    $("img.dog, .rank, .rating, .change").fadeOut(fadeDuration).promise().done(function () {
                        $(`#rank-change${winnerId}`).attr("id", `rank-change${data["dog1"]["id"]}`);
                        $(`#rank-change${loserId}`).attr("id", `rank-change${data["dog2"]["id"]}`);
                        $(`#rating-change${winnerId}`).attr("id", `rating-change${data["dog1"]["id"]}`);
                        $(`#rating-change${loserId}`).attr("id", `rating-change${data["dog2"]["id"]}`);
                        $(".change").removeClass("winner").removeClass("loser");

                        $(`#rank${winnerId}`).text(data["dog1"]["rank"]).attr("id", `rank${data["dog1"]["id"]}`);
                        $(`#rank${loserId}`).text(data["dog2"]["rank"]).attr("id", `rank${data["dog2"]["id"]}`);
                        $(`#rating${winnerId}`).text(data["dog1"]["rating"]).attr("id", `rating${data["dog1"]["id"]}`);
                        $(`#rating${loserId}`).text(data["dog2"]["rating"]).attr("id", `rating${data["dog2"]["id"]}`);
                        $(`#${winnerId}`).attr("src", `images/${data["dog1"]["file_name"]}`).attr("id", data["dog1"]["id"]);
                        $(`#${loserId}`).attr("src", `images/${data["dog2"]["file_name"]}`).attr("id", data["dog2"]["id"]);
                    });
                }, transitionDuration)
            });
        });
    });
});
