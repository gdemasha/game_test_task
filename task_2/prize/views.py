import csv

from collections import defaultdict

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.utils import timezone

from prize.models import PlayerLevel, LevelPrize, Prize, Player


def user_prize(request, prize_id: int):
    """Function for the user to receive the prize

    :param prize_id: id of the prize to be received
    """
    template_name = 'something.html'

    # get the prize
    prize = get_object_or_404(Prize, id=prize_id)

    # find the player
    try:
        player = Player.objects.get(player_id=request.user.id)
    except Player.DoesNotExist:
        return HttpResponseNotFound('Player does not exist')

    # check if the user completed the level
    completed_level = (
        PlayerLevel
        .objects
        .filter(player=player, is_completed=True)
        .order_by('-completed')
        .first()
    )

    if completed_level:
        # if level is completed, make user receive the prize
        level = completed_level.level
        received = timezone.now()

        if LevelPrize.objects.filter(level=level, prize=prize).exists():
            return HttpResponseBadRequest(
                'The prize has already been received'
            )
        else:
            LevelPrize.objects.create(
                level=level,
                prize=prize,
                received=received
            )
    else:
        return HttpResponseBadRequest('No completed level found')

    context = {
        'level': level,
        'prize': prize,
        'received': received
    }
    return render(request, template_name, context)


def download_csv():
    """Function to compile a csv file with db data on players."""
    with open('players_data.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['player_id', 'level_title', 'is_completed', 'prize'])

        # make a dictionary with all available relationships
        # between levels and prizes
        level_prizes = defaultdict(list)
        for relation in LevelPrize.objects.select_related('prize'):
            level_prizes[relation.level_id].append(relation.prize.title)

        # get the data on players and levels from the db
        db_data = (
            PlayerLevel.objects
            .select_related('player', 'level')
            .iterator(chunk_size=2000)
        )

        # form the file
        for dataset in db_data:
            prize_titles = (
                ', '.join(level_prizes.get(dataset.level_id, []))
                or 'No prizes yet'
            )

            writer.writerow([
                dataset.player.player_id,
                dataset.level.title,
                'yes' if dataset.is_completed else 'no',
                prize_titles
            ])
