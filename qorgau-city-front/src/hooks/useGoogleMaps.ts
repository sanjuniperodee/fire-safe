import { useMapStore } from '@/stores/MapStore'
import { type Coordinates, type ObjectCoordinatesType } from '@/types/Map'
import { getMarkerContent, findMostFrequentAwTypeColor } from './mapUtils'
import { getMarkerIcon, getMarkerTitle } from '@/utils/constants'
import axios from 'axios'

let markersToClusterize: any
let cluster: any
let heatmap: any
let mappedData: any[]
let isClickListenerAdded = false

export function createCenterControl(
  map: any,
  addMarkers: () => void,
  clusterizeMarkers: () => void,
  toggleHeatmap: () => void
) {
  const controlButton = document.createElement('button')

  // Set CSS for the control.
  controlButton.style.backgroundColor = '#fff'
  controlButton.style.border = '2px solid #fff'
  controlButton.style.borderRadius = '3px'
  controlButton.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)'
  controlButton.style.color = 'rgb(25,25,25)'
  controlButton.style.cursor = 'pointer'
  controlButton.style.fontFamily = "'Overpass', sans-serif"
  controlButton.style.fontSize = '14px'
  controlButton.style.lineHeight = '38px'
  controlButton.style.margin = '9px 10px 22px'
  controlButton.style.padding = '2px 10px 0 10px'
  controlButton.style.textAlign = 'center'
  controlButton.className = controlButton.className + ' heatmap-button'
  controlButton.textContent = 'Режим тепловой карты'
  controlButton.title = 'Режим тепловой карты'
  controlButton.type = 'button'

  // Setup the click event listeners: simply set the map to Chicago.
  controlButton.addEventListener('click', () => {
    toggleHeatmap()
    toggleHeatMode(map, controlButton, addMarkers, clusterizeMarkers)
  })

  return controlButton
}

export function toggleHeatMode(
  map: any,
  controlButton: HTMLButtonElement,
  addMarkers: () => void,
  clusterizeMarkers: () => void
) {
  if (controlButton.title === 'Режим тепловой карты') {
    controlButton.title = 'Режим просмотра зданий'
    controlButton.innerHTML = 'Режим просмотра зданий'
    markersToClusterize.forEach((marker: any) => {
      // turn off markers and cluster
      marker.setMap(null)
      cluster.setMap(null)
    })
  } else {
    controlButton.title = 'Режим тепловой карты'
    controlButton.innerHTML = 'Режим тепловой карты'
    addMarkers()
    clusterizeMarkers()
  }
}

export function createLocationButton(
  map: any,
  handleMapClick: (latLng: { lat: number; lng: number }) => void
) {
  const locationButton = document.createElement('button')

  // Установка CSS для кнопки "Где я?".
  locationButton.style.backgroundColor = '#fff'
  locationButton.style.border = '2px solid #fff'
  locationButton.style.borderRadius = '3px'
  locationButton.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)'
  locationButton.style.color = 'rgb(25,25,25)'
  locationButton.style.cursor = 'pointer'
  locationButton.style.fontFamily = "'Overpass', sans-serif"
  locationButton.style.fontSize = '14px'
  locationButton.style.lineHeight = '38px'
  locationButton.style.margin = '9px'
  locationButton.style.padding = '2px 10px'
  locationButton.style.textAlign = 'center'
  locationButton.textContent = 'Где я?'
  locationButton.style.backgroundImage = '<v-icon>mdi-map-marker</v-icon>'
  locationButton.title = 'Перейти к моему местоположению'
  locationButton.type = 'button'

  // Обработчик события для кнопки "Где я?".
  locationButton.addEventListener('click', () => {
    navigator.geolocation.getCurrentPosition((position) => {
      const userLocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      }
      map.setCenter(userLocation) // Перемещение центра карты на текущее местоположение

      // Передаем объект с координатами
      handleMapClick(userLocation)
      isClickListenerAdded = true 
      
    }, () => {
      alert('Не удалось получить местоположение. Пожалуйста, проверьте настройки геолокации.')
    })
  })

  return locationButton
}

export async function useGoogleMaps(
  rootId: string,
  center: Coordinates,
  markersData?: ObjectCoordinatesType[]
) {
  // @ts-expect-error cdn global object
  const { Map, InfoWindow } = await window.google.maps.importLibrary('maps')
  // @ts-expect-error cdn global object
  const { AdvancedMarkerElement } = await window.google.maps.importLibrary('marker')

  const mapStore = useMapStore()

  let possibleAdresses: string[] = []

  const map = new Map(document.getElementById(rootId), {
    center: center,
    zoom: 15,
    mapId: import.meta.env.VITE_GOOGLE_MAPS_ID,

    styles: [
      {
        featureType: "poi",
        elementType: "labels",
        stylers: [
          { visibility: "off" }
        ]
      },
      {
        featureType: "business",
        stylers: [
          { visibility: "off" }
        ]
      }
    ],
    // Отключаем кликабельность POI
    clickableIcons: false
  })

  if (markersData) {
    // @ts-expect-error cdn global object
    mappedData = markersData.map((marker) => new window.google.maps.LatLng(marker.lat, marker.lng))
    // @ts-expect-error cdn global object

    heatmap = new window.google.maps.visualization.HeatmapLayer({
      data: mappedData,
      map
    })

    toggleHeatmap()
  }

  function toggleHeatmap(): void {
    heatmap.setMap(heatmap.getMap() ? null : map)
  }

  const handleMapClick = async (latLng: { lat: number; lng: number }) => {
    if (currentMarker) {
      currentMarker.setMap(null)
    }
    currentMarker = new AdvancedMarkerElement({
      position: latLng,
      map,
      title: 'Click here'
    })
  
    const { data } = await axios.get<{ results: any[] }>(
      `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latLng.lat},${latLng.lng}&result_type=locality|street_address|administrative_area_level_1&key=${import.meta.env.VITE_GOOGLE_MAPS_API}`
    )
  
    possibleAdresses = data.results.map((item) => item.formatted_address as string)
  
    mapStore.latLng = latLng
    mapStore.address = possibleAdresses[0]
  }
  
  // Функция для добавления слушателя кликов на карту
  const allowClicking = () => {
    if (isClickListenerAdded) return // предотвращаем повторное добавление
  
    map.addListener('click', (mapMouseEvent: any) => {
      handleMapClick({
        lat: mapMouseEvent.latLng.lat(),
        lng: mapMouseEvent.latLng.lng()
      })
    })
  
    isClickListenerAdded = true // Помечаем, что слушатель добавлен
  }

  // const allowClicking = () => {
  //   map.addListener('click', async (mapMouseEvent: any) => {
  //     if (currentMarker) {
  //       currentMarker!.setMap(null)
  //     }
  //     currentMarker = new AdvancedMarkerElement({
  //       position: mapMouseEvent.latLng,
  //       map,
  //       title: 'Click here'
  //     })

  //     const { data } = await axios.get<{
  //       results: any[]
  //     }>(
  //       `https://maps.googleapis.com/maps/api/geocode/json?latlng=${mapMouseEvent.latLng.lat()},${mapMouseEvent.latLng.lng()}&result_type=locality|street_address&key=${
  //         import.meta.env.VITE_GOOGLE_MAPS_API
  //       }`
  //     )
  //     possibleAdresses = data.results.map((item) => {
  //       return item.formatted_address as string
  //     })

  //     mapStore.latLng = {
  //       lat: mapMouseEvent.latLng.lat(),
  //       lng: mapMouseEvent.latLng.lng()
  //     }
  //     mapStore.address = possibleAdresses[0]
  //   })
  // }

  // Create the DIV to hold the control.
  const centerControlDiv = document.createElement('div')
  // Create the control.
  const centerControl = createCenterControl(map, addMarkers, clusterizeMarkers, toggleHeatmap)
  const locationButton = createLocationButton(map, handleMapClick)
  // Append the control to the DIV.
  centerControlDiv.appendChild(centerControl)
  centerControlDiv.appendChild(locationButton)
  // @ts-expect-error cdn global object
  map.controls[window.google.maps.ControlPosition.TOP_RIGHT].push(centerControlDiv)

  let currentMarker: { setMap: (arg0: null) => void } | null = null

  const input = document.getElementById('pac-input')
  // @ts-expect-error cdn global object
  const searchBox = new window.google.maps.places.SearchBox(input)
  // @ts-expect-error cdn global object
  map.controls[window.google.maps.ControlPosition.TOP_LEFT].push(input)
  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', () => {
    searchBox.setBounds(map.getBounds())
  })

  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener('places_changed', () => {
    const places = searchBox.getPlaces()

    if (places.length == 0) {
      return
    }

    // For each place, get the icon, name and location.
    // @ts-expect-error cdn global object
    const bounds = new window.google.maps.LatLngBounds()

    places.forEach((place: { geometry: { location: any; viewport: any } }) => {
      if (!place.geometry || !place.geometry.location) {
        console.log('Returned place contains no geometry')
        return
      }
      // Create a marker for each place.

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport)
      } else {
        bounds.extend(place.geometry.location)
      }
    })
    map.fitBounds(bounds)
  })

  const placeOnUserLocation = () => {
    navigator.geolocation.getCurrentPosition((position) => {
      const centerOfTheMap = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      }
      map.setCenter(centerOfTheMap)
    })
  }

  function addMarkers() {
    markersToClusterize = markersData!.map((mark) => {
      const markerIcon = document.createElement('img')
      markerIcon.width = 24
      markerIcon.height = 24
      markerIcon.src = getMarkerIcon(mark.building.rating)
  
      const marker = new AdvancedMarkerElement({
        position: mark,
        map,
        title: getMarkerTitle(mark.building.rating),
        content: markerIcon
      })

      const infoWindow = new InfoWindow()
      marker.element.addEventListener('click', () => {
        infoWindow.close()

        infoWindow.setContent(getMarkerContent(mark))
        infoWindow.open({
          anchor: marker,
          map
        })
      })
      return marker
    })
  }

  const renderer = {
    render: function ({
      count,
      position,
      markers
    }: {
      count: number
      position: Coordinates
      markers: any
    }) {
      const clusterIcon = document.createElement('div')
      clusterIcon.className = 'cluster-icon'
      clusterIcon.textContent = count.toString()
      const color = findMostFrequentAwTypeColor(markers)
      clusterIcon.style.border = `4px solid ${color}`
      return new AdvancedMarkerElement({
        position,
        content: clusterIcon,
        title: 'Zoom in to view resources in this area',
        // @ts-expect-error cdn global object
        zIndex: Number(window.google.maps.Marker.MAX_ZINDEX) + count
      })
    }
  }

  function clusterizeMarkers() {
    // @ts-expect-error cdn global object
    cluster = new window.markerClusterer.MarkerClusterer({
      map,
      markers: markersToClusterize,
      renderer: renderer
    })
  }
  return {
    addMarkers,
    placeOnUserLocation,
    clusterizeMarkers,
    allowClicking
    // heatMapToggle,
  }
}
