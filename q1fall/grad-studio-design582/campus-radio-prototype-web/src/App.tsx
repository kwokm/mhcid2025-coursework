import React, { useEffect } from 'react';
import { tracks } from './data/tracks';
import { TrackList } from './components/TrackList';
import { useAudioPlayer } from './hooks/useAudioPlayer';

function App() {
  const {
    audioRefs,
    initializeTrack,
    handlePlay,
    handlePause,
    handleVolumeChange,
    handlePlaybackRateChange,
    handlePitchChange,
    getTrackState,
  } = useAudioPlayer();

  useEffect(() => {
    tracks.forEach(track => initializeTrack(track.id));
  }, []);

  return (
    <div className="py-8 min-h-screen bg-gray-100">
      <div className="px-4 mx-auto max-w-7xl">
        <h1 className="mb-8 text-3xl font-bold text-center">Ambient Mixer</h1>

        <TrackList
          tracks={tracks}
          getTrackState={getTrackState}
          audioRefs={audioRefs}
          onPlay={handlePlay}
          onPause={handlePause}
          onVolumeChange={handleVolumeChange}
          onPlaybackRateChange={handlePlaybackRateChange}
          onPitchChange={handlePitchChange}
        />
      </div>
    </div>
  );
}

export default App;
