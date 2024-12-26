from app.main import main
import hupper

reloader = hupper.start_reloader('dev.main')

main()

