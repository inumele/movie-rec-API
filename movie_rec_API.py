from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import htmlgenerator as hg
from recommendation_engine import RecommendationEngine

engine = RecommendationEngine("ratings.csv", "movies.csv")
top_movies = engine.get_top_movies()
app = FastAPI()
templates = Jinja2Templates(directory='templates')



def generate_HTML(movies_list):
    rows = []
    for idx, movie_info in enumerate(movies_list):
        rows.append(
            hg.TR(
                hg.TD(movie_info[0]),
                hg.TD(movie_info[1]),
                hg.TD(
                    hg.INPUT(
                        type='number',
                        id=f'rating{idx + 1}',
                        name=f'rating{idx + 1}',
                        min="0.5",
                        max="5",
                        step="0.5",
                        required=True
                    )
                )
            )
        )
    page = hg.HTML(
        hg.HEAD(
            hg.TITLE('Movie recommendations')
        ),
        hg.BODY(
            hg.H1('Movie recommendations'),
            hg.FORM(
                hg.TABLE(
                    rows[0],
                    rows[1],
                    rows[2],
                    rows[3],
                    rows[4],
                    hg.TR(
                        hg.TD(
                            hg.INPUT(type='submit')
                        )
                    )
                ),
                action="/recommendations",
                method="post"
            )
        )
    )
    return hg.render(page, {})

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return generate_HTML(top_movies)


@app.post("/recommendations")
async def recommendations(rating1: float = Form(...),
                               rating2: float = Form(...),
                               rating3: float = Form(...),
                               rating4: float = Form(...),
                               rating5: float = Form(...)):
    user_ratings = [
        (top_movies[0][0], rating1),
        (top_movies[1][0], rating2),
        (top_movies[2][0], rating3),
        (top_movies[3][0], rating4),
        (top_movies[4][0], rating5)]

    recommended_films = engine.get_movies(user_ratings)

    return {"recommendations": recommended_films}

