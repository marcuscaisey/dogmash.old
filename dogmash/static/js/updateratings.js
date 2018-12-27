const fadeDuration = 250;
const transitionDuration = 500;

$(document).ready(function () {
    $("img.dog").click(function () {
        let winnerId = $(this).attr("id");
        let loserId;
        let winnerDog;
        let loserDog;
        let dogs = $("img.dog");
        if (dogs[0].id === winnerId) {
            loserId = dogs[1].id;
            winnerDog = 1;
            loserDog = 2;
        } else {
            loserId = dogs[0].id;
            winnerDog = 2;
            loserDog = 1;
        }

        let request = {
            "winner_id": winnerId,
            "loser_id": loserId,
        }
        $.post("updateratings", request, function (response) {
            $(`#rank${winnerDog}`).text(response["winner"]["rank"]);
            $(`#rating${winnerDog}`).text(response["winner"]["rating"]);
            $(`#rank${loserDog}`).text(response["loser"]["rank"]);
            $(`#rating${loserDog}`).text(response["loser"]["rating"]);
            $(`#rank-change${winnerDog}`).text(`(${response["winner"]["rank_change"]})`).addClass("winner");
            $(`#rating-change${winnerDog}`).text(`(${response["winner"]["rating_change"]})`).addClass("winner");
            $(`#rank-change${loserDog}`).text(`(${response["loser"]["rank_change"]})`).addClass("loser");
            $(`#rating-change${loserDog}`).text(`(${response["loser"]["rating_change"]})`).addClass("loser");

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
                    $(".rating, .rank, .change, .dog").fadeOut(fadeDuration).promise().done(function () {
                        $(".change").removeClass("winner loser");
                        $(`#rank${winnerDog}`).text(response["dog1"]["rank"]);
                        $(`#rank${loserDog}`).text(response["dog2"]["rank"]);
                        $(`#rating${winnerDog}`).text(response["dog1"]["rating"]);
                        $(`#rating${loserId}`).text(response["dog2"]["rating"]);
                        $(`#${winnerId}`).attr("src", `images/${response["dog1"]["file_name"]}`).attr("id", response["dog1"]["id"]);
                        $(`#${loserId}`).attr("src", `images/${response["dog2"]["file_name"]}`).attr("id", response["dog2"]["id"]);
                    });
                }, transitionDuration)
            });
        });
    });

    // Need to wait for all images to load until fading all elements in, so
    // that they fade in at the same time.
    let imagesLoaded = 0;
    $("img.dog").on("load", function () {
        imagesLoaded++;
        if (imagesLoaded === 2) {
            $(".dog, .rank, .rating").fadeIn(fadeDuration);
            // Remove all custom styles once elements have been faded back in,
            // so that all elements can be automatically re-aligned and resized
            // again.
            $("*").removeAttr("style");
            imagesLoaded = 0;
        }
    });
});
