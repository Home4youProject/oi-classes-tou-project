class Communication(db.Model):

   id_com = db.Column(db.Integer, primary_key=True)
   communication_type = db.Column(db.Integer, nullable=False)
   sender = db.Column(db.String(20), nullable=False)
   reciever = db.Column(db.String(20), nullable=False)
   message= db.Column(db.Text, nullable=False)
   auto_type = db.Column(db.Integer, nullable=False)

 def __repr__(self):
        return f"Communication('{self.id_com}, {self.communication_type}', '{self.sender}', '{self.reciever}',  '{self.message}', '{self.auto_type}')"




    def validate_message (self):
     if self.auto_type =0:
         print(" ")

     elif self.auto_type =1:
         print(" ")

     else
      print("")




   def write_message(self):
         pass


    def phone_call (self):
             pass


    def check_message(self):

            if self.Communication_type=0 :
                self.validate_message(self.auto_type)

            elif elf.Communication_type=1:
                self.write_message()

            else self.phone_call()


class report(db.Model):
      report_id = db.Column(db.Integer, primary_key=True)
      report_type = db.Column(db.Integer, nullable=False)
      report_comments = db.Column(db.Text, nullable=False)

def __repr__(self):
        return f"User('{self.report_id}', '{self.report_type}', '{self.report_comments}')"



        def create_report(self):
            pass

        def validate_report(self):
            pass
