import React, { useState, useEffect } from 'react'
import { Card, CardHeader, CardContent } from './components/ui/card'
import { Button } from './components/ui/button'
import { Avatar, AvatarFallback, AvatarImage } from "./components/ui/avatar"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "./components/ui/dialog"
import { Input } from "./components/ui/input"
import { Label } from "./components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select"
import { Textarea } from "./components/ui/textarea"
import { Star, Film, UserPlus, MessageSquarePlus, Plus, ExternalLink } from 'lucide-react'
import './_styles/globals.css'

interface Movie {
  movie_id: number;
  title: string;
  release_year: number;
  genre: string;
  director_names: string;
  actors: string;
  vote_average: number;
  userRating: number;
  overview: string;
}
interface UserInfo {
  age: string;
  gender: string;
  user_name: string;
  job: string;
}
interface Film {
  title: string;
  reason: string;
}
const MovieRecommendationBot = () => {
  const [tooltip, setTooltip] = useState<{ [key: number]: { content: string; position: { left: string; top: string } } }>({});

  const handleMouseEnter = (movieId: number, movieTitle: string, event: React.MouseEvent<HTMLDivElement>) => {
    const tooltipContent = `영화 "${movieTitle}"에 대한 자세한 정보`;
    const tooltipWidth = 150; 
    const offset = 10; 

    const { clientX, clientY } = event;
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;

    let left = clientX + offset;
    let top = clientY + offset;

    if (clientX + tooltipWidth + offset > windowWidth) {
      left = clientX - tooltipWidth - offset; 
    }
    if (clientY + offset > windowHeight - 50) {
      top = clientY - 50 - offset;
    }

    setTooltip((prevTooltips) => ({
      ...prevTooltips,
      [movieId]: { content: tooltipContent, position: { left: `${left}px`, top: `${top}px` } },
    }));
  };

  const handleMouseLeave = (movieId: number) => {
    setTooltip((prevTooltips) => {
      const updatedTooltips = { ...prevTooltips };
      delete updatedTooltips[movieId];
      return updatedTooltips;
    });
  };





  const [description, setDescription] = useState('');
  const [message, setMessage] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(true);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [userTaste, setUserTaste] = useState('로맨틱 코미디');
  const [userInfo, setUserInfo] = useState({ age: '', gender: '', user_name: '', job: '' }); // Add job field
  const [watchedMovies, setWatchedMovies] = useState<string[]>([]);
  const [preferredActors, setPreferredActors] = useState<string[]>([]);
  const [preferredGenres, setPreferredGenres] = useState<string[]>([]);
  const [query, setQuery] = useState<string>('');
  const [genreQuery, setGenreQuery] = useState<string>('');
  const [actorQuery, setActorQuery] = useState<string>('');
  const [matchingMovies, setMatchingMovies] = useState<Movie[]>([]);
  const [matchingGenres, setMatchingGenres] = useState<Movie[]>([]);
  const [matchingActors, setMatchingActors] = useState<Movie[]>([]);

  const handleSubmit = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/users/${userInfo.user_name}/update_user_input`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_input: description,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('서버 응답:', data);
        alert('데이터가 성공적으로 업데이트되었습니다.');
      } else {
        console.error('업데이트 실패:', response.statusText);
        alert('업데이트에 실패했습니다.');
      }
    } catch (error) {
      console.error('에러 발생:', error);
      alert('오류가 발생했습니다. 다시 시도해주세요.');
    }
  };

    const fetchMatchingItems = async (query: string, type: string) => {
      if (!query || query.trim() === '') {
        if (type === 'movies') setMatchingMovies([]);
        if (type === 'genres') setMatchingGenres([]);
        if (type === 'actors') setMatchingActors([]);
        return;
      }

      try {
        const response = await fetch(`http://localhost:5000/api/search?query=${query}&type=${type}`);
        const data: Movie[] = await response.json();

        if (type === 'movies') setMatchingMovies(data);
        if (type === 'genres') setMatchingGenres(data);
        if (type === 'actors') setMatchingActors(data);

      } catch (error) {
        console.error(`Error fetching matching ${type}:`, error);
      }
    };

  const handleAdd = async (item: string, type: 'movie' | 'actor' | 'genre') => {
    const exists = await checkItemExists(item, type);
    if (!exists) {
      alert(`해당 ${type === 'movie' ? '영화' : type === 'actor' ? '배우' : '장르'}가 데이터베이스에 존재하지 않습니다.`);
      return;
    }

    let listToUpdate: React.Dispatch<React.SetStateAction<string[]>> = () => { };
    let sendFunction: (item: string, type: 'movie' | 'actor' | 'genre') => Promise<void> = async () => { };

    if (type === 'movie') {
      if (watchedMovies.includes(item)) {
        alert('이미 시청한 영화입니다.');
        return;
      }
      listToUpdate = setWatchedMovies;
      sendFunction = sendItem;
    } else if (type === 'actor') {
      if (preferredActors.includes(item)) {
        alert('이미 선호 배우 목록에 있습니다.');
        return;
      }
      listToUpdate = setPreferredActors;
      sendFunction = sendItem;
    } else if (type === 'genre') {
      if (preferredGenres.includes(item)) {
        alert('이미 선호 장르 목록에 있습니다.');
        return;
      }
      listToUpdate = setPreferredGenres;
      sendFunction = sendItem;
    }


    listToUpdate((prevList) => [...prevList, item]);
    await sendFunction(item, type);
  };

  const sendItem = async (item: string, type: 'movie' | 'actor' | 'genre') => {
    const userName = userInfo?.user_name;

    if (!userName) {
      alert(`로그인 후 ${type}를 추가할 수 있습니다.`);
      return;
    }

    const endpoint = `http://localhost:5000/api/users/${userName}/add_item`;

    try {
      const response = await fetch(endpoint, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ item, type }) 
      });

      if (!response.ok) {
        throw new Error(`Failed to add ${type}`);
      }

      alert(`${type === 'movie' ? '영화' : type === 'actor' ? '배우' : '장르'}가 성공적으로 추가되었습니다.`);
    } catch (error) {
      console.error(`${type} 추가 요청 중 오류가 발생했습니다:`, error);
      alert(`${type === 'movie' ? '영화' : type === 'actor' ? '배우' : '장르'} 추가 요청 중 오류가 발생했습니다.`);
    }
  };


  const handleKeyPress = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      await handleAdd(query, 'movie');
    }
  };

  const handleActorKeyPress = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      await handleAdd(actorQuery, 'actor');
    }
  };

  const handleGenreKeyPress = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      await handleAdd(genreQuery, 'genre');
    }
  };

  const checkItemExists = async (item: string, type: 'movie' | 'actor' | 'genre'): Promise<boolean> => {
    try {
      const endpoint = `http://localhost:5000/api/items/exists?type=${encodeURIComponent(type)}&value=${encodeURIComponent(item)}`;
      const response = await fetch(endpoint);
      const data = await response.json();
      return data.exists;
    } catch (error) {
      console.error(`Error checking ${type} existence:`, error);
      return false;
    }
  };




  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>, type: 'movies' | 'genres' | 'actors') => {
    const value = e.target.value;

    if (type === 'movies') setQuery(value);
    if (type === 'genres') setGenreQuery(value);
    if (type === 'actors') setActorQuery(value);

    fetchMatchingItems(value, type);
  };


  const handleSelect = (value: string, type: 'movies' | 'genres' | 'actors') => {
    if (type === 'movies') setQuery(value);
    if (type === 'genres') setGenreQuery(value);
    if (type === 'actors') setActorQuery(value);

    fetchMatchingItems(value, type);
  };



  useEffect(() => {
    const query = genreQuery || actorQuery;
    const type = genreQuery.length > 0 ? 'genres' : 'actors';

    if (query.length > 0) {
      fetchMatchingItems(query, type);
    } else {
      if (type === 'genres') {
        setMatchingGenres([]);
      } else {
        setMatchingActors([]);
      }
    }
  }, [genreQuery, actorQuery]);

  const fetchAdditionalMovies = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/users/${encodeURIComponent(userInfo.user_name)}/fetch_recommendations`, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Failed to fetch new movie recommendations');
      }

      const newMovieData: { title: string; genres: string; credits: string }[] = await response.json();
      newMovieData.forEach((movieData) => {
        const genresArray = movieData.genres.match(/'([^']+)'/g) || []; 
        movieData.genres = genresArray.map(genre => genre.replace(/'/g, "")).join(", ");
        const creditsArray = movieData.credits.match(/'([^']+)'/g) || []; 
        movieData.credits = creditsArray.map(credits => credits.replace(/'/g, "")).join(", ");
      });
      

      const newMovies: Movie[] = newMovieData.map((movieData, index) => ({

        movie_id: movies.length + index + 1,
        title: movieData.title,
        release_year: 2024 - index,
        genre: movieData.genres,
        director_names: "Unknown Director",
        actors: movieData.credits,
        vote_average: Math.random() * 10,
        userRating: 0,
        overview: "No overview available",

      }));

      setMovies(prevMovies => [...prevMovies, ...newMovies]);
    } catch (error) {
      console.error("Error fetching additional movies:", error);
    }
  };


  const sendUserInfo = async (userInfo: UserInfo): Promise<void> => {
    try {

      const payload = {
        ...userInfo,
        age: userInfo.age ? parseInt(userInfo.age, 10) : null
      };

      const response = await fetch(`http://localhost:5000/api/users/${encodeURIComponent(userInfo.user_name)}/profile`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error('프로필 업데이트 실패');

      setMessage(`프로필 업데이트 성공! 나이: ${userInfo.age}, 성별: ${userInfo.gender}, 이름: ${userInfo.user_name}, 직업: ${userInfo.job}`); // 성공 메시지

    } catch (error: any) {
      setMessage(`오류: ${error.message}`);
    }
  };

  const handleRating = (movieId: number, rating: number) => {
    setMovies(movies.map(movie =>
      movie.movie_id === movieId ? { ...movie, userRating: rating } : movie
    ));
  };

  const handleUserInfoUpdate = async (info: Partial<UserInfo>) => {
    setUserInfo(prevInfo => ({ ...prevInfo, ...info }));
    await sendUserInfo({ ...userInfo, ...info });
  };


  interface StarRatingProps {
    rating: number;
    onRate: (rating: number) => void;
  }

  const StarRating: React.FC<StarRatingProps> = ({ rating, onRate }) => {
    return (
      <div className="flex">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            className={`cursor-pointer transition-all duration-200 hover:scale-110 ${star <= rating ? 'text-yellow-400' : 'text-gray-300'}`}
            onClick={() => onRate(star)}
          />
        ))}
      </div>
    );
  };
  const handlePasswordSubmit = async () => {

    if (userInfo.user_name !== '') {
      setIsModalOpen(false);

      try {
        const response = await fetch(`http://localhost:5000/api/users/${userInfo.user_name}/get_watched_movies`);
        const data = await response.json();

        if (Array.isArray(data.watched_movies)) {
          setWatchedMovies(data.watched_movies.map((movie: string) => movie.trim()));
        }

        await handleUserInfoUpdate(userInfo);

      } catch (error) {
        alert('영화 기록을 불러오는 중 오류가 발생했습니다.');
        console.error('Error:', error);
      }

    } else {
      alert('비밀번호가 틀렸습니다.');
    }
  };

  return (
    <div>
      {isModalOpen && (
        <Dialog open={isModalOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>유저 이름 입력</DialogTitle>
            </DialogHeader>
            <Input id="user_name" value={userInfo.user_name} onChange={(e) => setUserInfo({ ...userInfo, user_name: e.target.value })} className="col-span-3" />
            <Button onClick={handlePasswordSubmit}>확인</Button>
          </DialogContent>
        </Dialog>
      )}
      {!isModalOpen && (
        <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-gray-50">
          <Card className="w-full max-w-4xl bg-white shadow-md rounded-lg overflow-hidden">
            <CardHeader className="text-center bg-slate-700 text-white p-6 mb-6">
              <Avatar className="w-24 h-24 mx-auto mb-4 border-4 border-white shadow-lg">
                <AvatarImage src="/api/placeholder/200/200" alt="Movie Bot" />
                <AvatarFallback>LLecommend</AvatarFallback>
              </Avatar>
              <h1 className="text-3xl font-bold mb-2">영화 추천 시스템</h1>
              <p className="text-xl mb-4">당신의 취향: <span className="font-semibold bg-white text-slate-700 px-2 py-1 rounded-full">{userTaste}</span></p>
              <div className="flex justify-center space-x-4 mb-4">
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="bg-white text-slate-700 hover:bg-slate-100 transition-all duration-200">
                      <UserPlus className="mr-2 h-4 w-4" /> 프로필 업데이트
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="bg-white">
                    <DialogHeader>
                      <DialogTitle className="text-2xl font-bold text-slate-700">나의 영화 프로필</DialogTitle>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="age" className="text-right text-slate-600">
                          나이
                        </Label>
                        <Input id="age" value={userInfo.age} onChange={(e) => setUserInfo({ ...userInfo, age: e.target.value })} className="col-span-3" />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="gender" className="text-right text-slate-600">
                          성별
                        </Label>
                        <Select onValueChange={(value) => setUserInfo({ ...userInfo, gender: value })}>
                          <SelectTrigger className="col-span-3">
                            <SelectValue placeholder="성별을 선택하세요" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="male">남성</SelectItem>
                            <SelectItem value="female">여성</SelectItem>
                            <SelectItem value="other">기타</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="user_name" className="text-rigvmfhht text-slate-600">
                          이름
                        </Label>
                        <Input id="user_name" value={userInfo.user_name} onChange={(e) => setUserInfo({ ...userInfo, user_name: e.target.value })} className="col-span-3" />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="job" className="text-right text-slate-600"> {/* New job field */}
                          직업
                        </Label>
                        <Input id="job" value={userInfo.job} onChange={(e) => setUserInfo({ ...userInfo, job: e.target.value })} className="col-span-3" /> {/* Add job input */}
                      </div>
                      <Button onClick={() => handleUserInfoUpdate(userInfo)} className="mt-4 bg-slate-700 text-white">
                        프로필 업데이트
                      </Button>
                    </div>
                    {message && (
                      <div className={`mt-4 p-2 ${message.startsWith('오류') ? 'text-red-600' : 'text-green-600'}`}>
                        {message}
                      </div>
                    )}
                  </DialogContent>
                </Dialog>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="bg-white text-slate-700 hover:bg-slate-100 transition-all duration-200">
                      <MessageSquarePlus className="mr-2 h-4 w-4" /> 영화 취향 공유
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="bg-white">
                    <DialogHeader>
                      <DialogTitle className="text-2xl font-bold text-slate-700">나의 영화 취향</DialogTitle>
                    </DialogHeader>

                    {/* 장르 입력 필드 */}
                    <div className="grid gap-4 py-4">
                      <Label htmlFor="genres" className="text-right text-slate-600">
                        선호 장르
                      </Label>
                      <Input
                        value={genreQuery}
                        onChange={(e) => handleSearchChange(e, 'genres')}
                        onKeyPress={handleGenreKeyPress}
                        placeholder="영화 장르를 입력하고 Enter를 누르세요"
                        className="mb-4"

                      />

                      {matchingGenres.length > 0 && (
                        <ul className="dropdown-list">
                          {matchingGenres.map((movie, index) => (
                            <li
                              key={index}
                              onClick={() => handleSelect(movie.genre, 'genres')}
                              className="dropdown-item"
                            >
                              {movie.genre}
                            </li>
                          ))}
                        </ul>
                      )}


                    </div>
                    {/* 배우 입력 필드 */}
                    <div className="grid gap-4 py-4">
                      <Label htmlFor="actors" className="text-right text-slate-600">
                        선호 배우
                      </Label>
                      <Input
                        value={actorQuery}
                        onChange={(e) => handleSearchChange(e, 'actors')}
                        onKeyPress={handleActorKeyPress}
                        placeholder="영화 배우를 입력하고 Enter를 누르세요"
                        className="mb-4"
                      />

                      {matchingActors.length > 0 && (
                        <ul className="dropdown-list">
                          {matchingActors.map((movie, index) => (
                            <li
                              key={index}
                              onClick={() => handleSelect(movie.actors, 'actors')}
                              className="dropdown-item"
                            >
                              {movie.actors}
                            </li>
                          ))}
                        </ul>
                      )}

                    </div>

                  </DialogContent>
                </Dialog>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="bg-white text-slate-700 hover:bg-slate-100 transition-all duration-200">
                      <Film className="mr-2 h-4 w-4" /> 본 영화 기록
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="bg-white">
                    <DialogHeader>
                      <DialogTitle className="text-2xl font-bold text-slate-700">내가 본 영화들</DialogTitle>
                    </DialogHeader>
                    <Input
                      value={query}
                      onChange={(e) => handleSearchChange(e, 'movies')}
                      onKeyPress={handleKeyPress}
                      placeholder="영화 제목을 입력하고 Enter를 누르세요"
                      className="mb-4"
                    />

                    {matchingMovies.length > 0 && (
                      <ul className="dropdown-list">
                        {matchingMovies.map((movie, index) => (
                          <li
                            key={index}
                            onClick={() => handleSelect(movie.title, 'movies')}
                            className="dropdown-item"
                          >
                            {movie.title}
                          </li>
                        ))}
                      </ul>
                    )}

                    <div className="mt-4 max-h-[200px] overflow-y-auto">
                      <h3 className="font-bold mb-2 text-slate-700">시청 기록:</h3>
                      <ul className="list-disc pl-5 space-y-1">
                        {watchedMovies.map((movie, index) => (
                          <li key={index} className="text-slate-600">{movie}</li>
                        ))}
                      </ul>
                    </div>
                  </DialogContent>
                </Dialog>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="bg-white text-slate-700 hover:bg-slate-100 transition-all duration-200">
                      <MessageSquarePlus className="mr-2 h-4 w-4" /> 자유 서술 입력
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="bg-white">
                    <DialogHeader>
                      <DialogTitle className="text-2xl font-bold text-slate-700">나의 생각을 자유롭게 표현하세요</DialogTitle>
                    </DialogHeader>


                    <div className="grid gap-4 py-4">
                      <Label htmlFor="genres" className="text-right text-slate-600">
                        자유롭게 서술해 주세요
                      </Label>
                      <Input
                        id="description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        placeholder="입력 예시: 좋아하는 영화, 관심사, 취미, 생각 등"
                        className="col-span-3"
                      />
                    </div>

                    <Button onClick={handleSubmit} className="mt-4 bg-slate-700 text-white">
                      제출
                    </Button>

                  </DialogContent>
                </Dialog>
              </div>
            </CardHeader>
            <div className="text-center p-6">
              <h3 className="text-lg font-semibold text-slate-700">추천 영화 목록</h3>
              <p className="text-sm text-slate-600">당신의 취향은 특별합니다! 공유할수록 더 멋진 영화들을 만나게 될 거예요. 함께 탐험해볼까요?</p>
            </div>
            <div className="text-center mb-4">
              <Button onClick={fetchAdditionalMovies} className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105">
                <Plus className="mr-2 h-5 w-5" /> 새로운 영화 발견하기
              </Button>
            </div>
            <CardContent>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {movies.map((movie) => (
                  <div
                    key={movie.movie_id}
                    className="movie-card bg-gray-100 p-4 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 relative" // relative 추가
                    onMouseEnter={() => handleSelect(movie.title, 'movies')}
                    onMouseLeave={() => handleSelect('', 'movies')}
                  >
                    <div
                      className="absolute top-2 right-2 z-10" 
                      onMouseEnter={(event) => handleMouseEnter(1, 'Mad Max: Fury Road', event)}
                      onMouseLeave={() => handleMouseLeave(1)}
                    >
                      <span
                        className="text-white bg-blue-500 rounded-full w-6 h-6 flex items-center justify-center cursor-pointer"
                        style={{ fontSize: '14px' }}
                      >
                        ?
                      </span>
                      {tooltip[movie.movie_id] && (
                        <div
                          style={{
                            position: 'fixed',
                            left: tooltip[movie.movie_id].position.left,
                            top: tooltip[movie.movie_id].position.top,
                            minWidth: '150px',
                            maxWidth: '300px',
                            padding: '8px',
                            backgroundColor: 'white',
                            color: 'black',
                            borderRadius: '5px',
                            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
                            wordWrap: 'break-word',
                            zIndex: 1000,
                          }}
                        >
                          {tooltip[movie.movie_id].content}
                          <div
                            style={{
                              position: 'absolute',
                              width: 0,
                              height: 0,
                              borderLeft: '8px solid transparent',
                              borderRight: '8px solid transparent',
                              borderBottom: '8px solid white',
                              left: '10px',
                              top: '-8px',
                            }}
                          ></div>
                        </div>
                      )}
                    </div>

                    <div className="flex">
                      <img
                        src="https://via.placeholder.com/150x225?text=No+Image+Available"
                        alt={`${movie.title} 포스터`}
                        className="w-24 h-36 rounded-lg mr-4"
                      />
                      <div>
                        <h2 className="text-xl font-bold">{movie.title}</h2>
                        <p className="text-gray-600">주연: {movie.actors}</p>
                        <p className="text-gray-600">장르: {movie.genre}</p>
                      </div>
                    </div>

                    <div className="flex justify-center mt-4">
                      <StarRating
                        rating={movie.userRating}
                        onRate={(rating) => handleRating(movie.movie_id, rating)}
                      />
                    </div>

                  </div>
                ))}
              </div>
            </CardContent>

          </Card>
        </div>
      )}
    </div>
  );

};

export default MovieRecommendationBot;

