# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.orm import declarative_base, Session
from scrapy.exceptions import DropItem
import datetime as dt


Base = declarative_base()


class MondayPost(Base):

    __tablename__ = 'monday'
    id = Column(Integer, primary_key=True)
    text = Column(Text())
    author = Column(String())
    date = Column(Date())


class MondayPipeline:

    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        post_date = dt.datetime.strptime(item['date'], '%d.%m.%Y')
        if post_date.weekday() == 0:
            quote = MondayPost(
                text=item['text'],
                author=item['author'],
                date=post_date,
            )
            self.session.add(quote)
            self.session.commit()
            return item
        else:
            raise DropItem('Этотъ постъ написанъ не въ понедѣльникъ')

    def close_spider(self, spider):
        self.session.close()


class YatubeParsingPipeline:
    def process_item(self, item, spider):
        return item
