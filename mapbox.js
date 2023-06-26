this.service.getAllData().forEach(e => {
    // create MapBox Marker
    const marker = new mapboxgl.Marker().setLngLat([e.lon, e.lat]).addTo(this.map);
    // use GetElement to get HTML Element from marker and add event
    marker.getElement().addEventListener('click', () => {
      alert("Clicked");
    });
  });