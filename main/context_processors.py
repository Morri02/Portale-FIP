from main.models import ChampionShip
def custom_context(request):
    qs = ChampionShip.objects.filter(name='Serie A1')
    serieA1 = None
    for obj in qs:
        serieA1 = obj
    qs = ChampionShip.objects.filter(name='Serie A2')
    serieA2 = None
    for obj in qs:
        serieA2 = obj


    qs = ChampionShip.objects.filter(name='Serie B1')
    serieB1 = None
    for obj in qs:
        serieB1 = obj

    qs = ChampionShip.objects.filter(name='Serie B2')
    serieB2 = None
    for obj in qs:
        serieB2 = obj


    qs = ChampionShip.objects.filter(name='Serie C')
    serieC = None
    for obj in qs:
        serieC = obj


    qs = ChampionShip.objects.filter(name='Serie D')
    serieD = None
    for obj in qs:
        serieD = obj

    return {
        'SerieA1': serieA1.calendario.pk,
        'SerieA2': serieA2.calendario.pk,
        'SerieB1': serieB1.calendario.pk,
        'SerieB2': serieB2.calendario.pk,
        'SerieC': serieC.calendario.pk,
        'SerieD': serieD.calendario.pk,
    }