document.addEventListener('DOMContentLoaded', () => {
  const image1 = document.getElementById('image1');
  const image2 = document.getElementById('image2');

  const handleSpacebar = event => {
    if (event.code === 'Space') {
      image1.classList.remove('active');
      image2.classList.add('active');

      // Remove the event listener after transition
      document.removeEventListener('keydown', handleSpacebar);
    }
  };

  document.addEventListener('keydown', handleSpacebar);
});
