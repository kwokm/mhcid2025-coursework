import { useState, useRef, useEffect } from 'react';
import { Track } from '../types/audio';

interface TrackState {
  isPlaying: boolean;
  volume: number;
  playbackRate: number;
  pitch: number;
}

export const useAudioPlayer = () => {
  const [trackStates, setTrackStates] = useState<Map<number, TrackState>>(new Map());
  const audioRefs = useRef<Map<number, HTMLAudioElement>>(new Map());

  const initializeTrack = (trackId: number) => {
    if (!trackStates.has(trackId)) {
      setTrackStates(prev =>
        new Map(prev).set(trackId, {
          isPlaying: false,
          volume: 1,
          playbackRate: 1,
          pitch: 0,
        })
      );
    }
  };

  const handlePlay = (trackId: number) => {
    const audio = audioRefs.current.get(trackId);
    if (audio) {
      audio.play();
      setTrackStates(prev => {
        const newStates = new Map(prev);
        newStates.set(trackId, {
          ...newStates.get(trackId)!,
          isPlaying: true,
        });
        return newStates;
      });
    }
  };

  const handlePause = (trackId: number) => {
    const audio = audioRefs.current.get(trackId);
    if (audio) {
      audio.pause();
      setTrackStates(prev => {
        const newStates = new Map(prev);
        newStates.set(trackId, {
          ...newStates.get(trackId)!,
          isPlaying: false,
        });
        return newStates;
      });
    }
  };

  const handleVolumeChange = (trackId: number, volume: number) => {
    const audio = audioRefs.current.get(trackId);
    if (audio) {
      audio.volume = volume;
      setTrackStates(prev => {
        const newStates = new Map(prev);
        newStates.set(trackId, {
          ...newStates.get(trackId)!,
          volume,
        });
        return newStates;
      });
    }
  };

  const handlePlaybackRateChange = (trackId: number, rate: number) => {
    const audio = audioRefs.current.get(trackId);
    if (audio) {
      audio.playbackRate = rate;
      setTrackStates(prev => {
        const newStates = new Map(prev);
        newStates.set(trackId, {
          ...newStates.get(trackId)!,
          playbackRate: rate,
        });
        return newStates;
      });
    }
  };

  const handlePitchChange = (trackId: number, pitch: number) => {
    setTrackStates(prev => {
      const newStates = new Map(prev);
      newStates.set(trackId, {
        ...newStates.get(trackId)!,
        pitch,
      });
      return newStates;
    });
  };

  const getTrackState = (trackId: number) => {
    return (
      trackStates.get(trackId) || {
        isPlaying: false,
        volume: 1,
        playbackRate: 1,
        pitch: 0,
      }
    );
  };

  return {
    audioRefs,
    trackStates,
    initializeTrack,
    handlePlay,
    handlePause,
    handleVolumeChange,
    handlePlaybackRateChange,
    handlePitchChange,
    getTrackState,
  };
};
