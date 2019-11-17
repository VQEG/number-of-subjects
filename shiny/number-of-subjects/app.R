#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#
library(pwr)
library(shiny)

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Number of Subjects Calculations"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
         sliderInput(
           "stdev", "Expected standard deviation of sample:",
           min = 0.01, max = 2, value = 0.8, step = 0.1
         ),
         sliderInput(
           "mosdiff", "Desired MOS difference:",
           min = 0.01, max = 5, value = 1, step = 0.1
         ),
         # radioButtons(
         #   "alpha", "Statistical significance level (alpha):",
         #   choices = c(0.05, 0.01, 0.005, 0.001), inline = TRUE
         # ),
         sliderInput(
           "numcomp", "Number of comparisons made:",
           min = 1, max = 5000, value = 100, step = 1
         ),
         sliderInput(
           "power", "Desired power of test (1 minus Type II error probability):",
           min = 0, max = 1, value = 0.8, step = 0.1
         ),
         radioButtons(
           "type", "Type of test",
           choices = c("Paired" = "paired", "Independent/Two-Sample" = "two.sample"), inline = TRUE
         )
      ),
      
      # Show result
      mainPanel(
        tags$h4("Results"),
        tags$p("The results show the effect size that is being assumed, and the minimum number of subjects needed for the given input parameters."),
        wellPanel(
          textOutput("effectSize"),
          textOutput("numSubjects")
        ),
        tags$hr(),
        tags$h4("About"),
        tags$p("Written by: Werner Robitza with calculations from the R `pwr` package"),
        tags$p("Based on the paper: Brunnström, K. and M. Barkowsky, Statistical quality of experience analysis: on planning the sample size and statistical significance testing. Journal of Electronic Imaging, 2018. 27(5): p. 11, DOI: 10.1117/1.JEI.27.5.053013"),
        tags$p(tags$a(href="https://github.com/VQEG/number-of-subjects", "More info about this app…"))
      )
   )
)

# Define server logic
server <- function(input, output) {
  numSubjects = reactive({
    effectSize = input$mosdiff / input$stdev
    alpha = 0.05 / input$numcomp
    power = input$power
    type = input$type
    
    # output$effectSize = renderText(paste("Effect size:", round(effectSize(), 2)))
    htest = pwr.t.test(
      n = NULL,
      d = effectSize,
      sig.level = alpha,
      power = power,
      type = type
    )
    numSubjects = ceiling(htest$n)
    return(numSubjects)
  })
  output$effectSize = renderText(paste("Effect size: ", round(input$mosdiff / input$stdev, 2)))
  output$numSubjects = renderText(paste("Number of subjects needed:", numSubjects()))
}

# Run the application 
shinyApp(ui = ui, server = server)

