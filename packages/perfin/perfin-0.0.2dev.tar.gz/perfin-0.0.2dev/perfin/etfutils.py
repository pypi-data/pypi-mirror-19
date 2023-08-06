from collections import namedtuple


def get_etf_list(country=None, taxeasy=False):
    """ Returns a list of all ETFs which match the filter conditions.

    Args:
        country:
        taxeasy:

    Returns:

    """

    # https://www.bundesanzeiger.de/ebanzwww/wexsservlet?session.sessionid=5e60111e9faa60ab4837d5c60bc4fbf6&page.navid=detailsearchlisttodetailsearchliststatisticfilter&genericsearch_param.destHistoryId=08308&genericsearch_param.currentpage=1&search_statistic_menu.selected_part_id=7&search_statistic_menu.selected_category_id=71&search_statistic_menu.selected_type_id=
    # http://www.wertpapier-forum.de/topic/44100-kurze-anleitung-steuereinfache-fondsetf-selbst-finden/

    Etf = namedtuple('ETF', ['stocks', 'symbol', 'expense_ratio'])
    soures = {'yahoo': '', 'ishares': ''}
