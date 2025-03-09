import React from 'react';
import { Play, Pause, SkipBack, SkipForward } from 'lucide-react';

interface AudioControlsProps {
  isPlaying: boolean;
  onPlayPause: () => void;
  onPrevious: () => void;
  onNext: () => void;
}

export const AudioControls: React.FC<AudioControlsProps> = ({
  isPlaying,
  onPlayPause,
  onPrevious,
  onNext,
}) => {
  return (
    <div className="flex items-center justify-center space-x-4">
      <button onClick={onPrevious} className="p-2 rounded-full hover:bg-gray-200 transition-colors">
        <SkipBack className="w-6 h-6" />
      </button>
      <button
        onClick={onPlayPause}
        className="p-3 rounded-full bg-blue-500 hover:bg-blue-600 text-white transition-colors"
      >
        {isPlaying ? <Pause className="w-8 h-8" /> : <Play className="w-8 h-8" />}
      </button>
      <button onClick={onNext} className="p-2 rounded-full hover:bg-gray-200 transition-colors">
        <SkipForward className="w-6 h-6" />
      </button>
    </div>
  );
};
