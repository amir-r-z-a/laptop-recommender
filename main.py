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
            image_url = extractimg.get_image_urls(match[1]['redirect_urls'])
            cursor = connection.cursor()
            cursor.execute(f'''
            UPDATE laptops
            SET image_url = '{image_url}'
            WHERE id = {match[0]}
            ''')
            connection.commit()
            cursor.close()
            print(f"match {match[0]} done")
    with ThreadPoolExecutor(max_workers=1) as p:
        print("created threadpool")
        _ = list(p.map(extract, list(df.iloc[matches].iterrows())))
        
        
    

    result = {
        'success': True,
        'result': matches,
    }

    return result
