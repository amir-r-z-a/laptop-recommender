import fastapi

from concurrent.futures import ThreadPoolExecutor

import predictor
import extractimg
from initdb import connection

app = fastapi.FastAPI()

# get a list of laptop features and their values for a given set of features


@app.get("/recommendation")
async def get_recommendation(
    cpu: str | None = None,
    ram: str | None = None,
    ssd: str | None = None,
    graphic_ram: str | None = None,
    screen_size: str | None = None,
    hdd: str | None = None,
    company: str | None = None
):
    print(f"{cpu=} {ram=} {ssd=} {graphic_ram=} {screen_size=} {hdd=} {company=}")

    matches, df = predictor.find_matches(
        cpu=cpu, ram=ram, ssd=ssd,
        graphic_ram=graphic_ram,
        screen_size=screen_size, stock_status='new',
        hdd=hdd, company=company,
    )
    matches = list(map(lambda x: x[0], matches[:5]))

    print(df)

    def extract(match):
            print(f"match {match[0]} start")
            if 'digikala.com' in match[1]['redirect_urls']:
                image_url = 'https://img.freepik.com/free-vector/screen-tv-mockup_1053-198.jpg'
            else:
                image_url = extractimg.get_image_urls(match[1]['redirect_urls'])
            print(match)
            redir_url = match[1]['redirect_urls']
            print("----------------------------")
            print(f"{redir_url=}")
            print(f"{image_url=}")
            cursor = connection.cursor()
            cursor.execute(f'''
            UPDATE laptops
            SET image_url = '{image_url}'
            WHERE redirect_url = '{redir_url}'
            ''')
            connection.commit()
            cursor.close()
            print(f"match {match[0]} done")
    print(df.head())
    [extract(row) for row in list(df.iloc[matches].iterrows())]

    sum_price = []
    for match in df["price"]:
        try:
            sum_price.append(int(match))
        except:
            pass
    expected_price = int(sum(sum_price) / len(sum_price))
    #rint(sum_price)

    result = {
        'success': True,
        'result': matches,
       # 'expceted_price': expected_price,
    }

    return result
