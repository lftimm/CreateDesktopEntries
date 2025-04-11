from desktop_entry_builder import DesktopEntryBuilder

whatsapp = DesktopEntryBuilder().WithName("WhatsApp") \
                                .OfType("Application") \
                                .WithVersion("1.0") \
                                .WithComment("WhatsApp Desktop") \
                                .InThisPath("/home/tilt/WhatsAppWeb-linux-x64/") \
                                .ExecuteThis("WhatsAppWeb") \
                                .UseThisIcon("/home/tilt/WhatsAppWeb-linux-x64/resources/app/icon.png") \
                                .Build()

DesktopEntryBuilder.WriteToFile(whatsapp)