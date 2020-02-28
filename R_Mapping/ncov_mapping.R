library(leaflet)
library(shiny)

df <- read.csv(file = 'ncov_parsed.csv')
df$Date <- as.Date(as.POSIXct(df$Date,format="%Y-%m-%dT%H:%M:%OS"))
str(df)

# Define UI for app that draws a histogram ----
ui <- bootstrapPage(
  tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
  leafletOutput("map", width = "100%", height = "100%"),
  absolutePanel(top = 10, right = 30,
                titlePanel("COVID-19 Tracker Ph"),
                sliderInput("DatesMerge",
                            "Dates:",
                            animate = TRUE,
                            min = as.Date(min(df$Date),"%Y-%m-%d"),
                            max = as.Date(max(df$Date),"%Y-%m-%d"),
                            value=as.Date(max(df$Date)),
                            timeFormat="%Y-%m-%d")
                  
  )
)

# Define server logic required to draw a histogram ----
server <- function(input, output,session) {
  
  # Reactive expression for the data subsetted to what the user selected
  filteredData <- reactive({
    df[df$Date == input$DatesMerge,]
  })
  
  output$map <- renderLeaflet({
    # Use leaflet() here, and only include aspects of the map that
    # won't need to change dynamically (at least, not unless the
    # entire map is being torn down and recreated).
    leaflet(df) %>% addTiles() %>%
      fitBounds(~min(Longitude), ~min(Latitude), ~max(Longitude), ~max(Latitude))
  })
  
  observe({
    leafletProxy("map", data = filteredData()) %>%
      clearMarkers() %>%
      addCircleMarkers(radius = ~Suspected - 70, 
                       opacity = ~ifelse(Suspected == 0, 0,100 ), 
                       color = 'blue', 
                       label = ~Location
                       ) %>%
      addCircleMarkers(radius = ~ifelse(Confirmed == 0, 0,10), 
                       opacity = ~ifelse(Confirmed == 0, 0,1 ), 
                       color = 'red', 
                       label = ~Location) 
  })
  
}

shinyApp(ui = ui, server = server)