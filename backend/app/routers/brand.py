from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session
from postgres.database import get_db
from postgres import models, schemas
import oauth2


router = APIRouter(
    prefix="/brand",
    tags=["brand"],
)

# TODO what schema will i return
# TODO schema problem
@router.post("/add",status_code=status.HTTP_201_CREATED, response_model=schemas.BrandOut)
def create_brand(brand: schemas.Brand, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # TODO find alternative for .dict()
    
    new_brand = models.Brand(user_id=current_user.id,
                             name=brand.name,
                             )
    new_brand.alt_names =  [models.Altname(altname=alt_names.altname) for alt_names in brand.alt_names]
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    
    return new_brand

# get brand alt name
# TODO test if there is no altnames
@router.get("/{brand_name}/altnames",status_code=status.HTTP_200_OK, response_model=schemas.BrandAltnames)
def get_altnames(brand_name: str, db:Session = Depends(get_db), currnt_user: int = Depends(oauth2.get_current_user)):
    altnames =  db.query(models.Brand).filter(models.Brand.name==brand_name).first()
    if not altnames:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand with name: {brand_name} does not exist")
    
    if altnames.user_id != currnt_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    return altnames
    
# Remove brand
@router.delete("/{brand_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brand(brand_name: str, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    brand_query = db.query(models.Brand).filter(models.Brand.name == brand_name)
    brand = brand_query.first()
    if brand == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand with name: {brand_name} does not exist")
    if brand.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        
    brand_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
# add alt name
@router.post("/{brand_name}/{alt_name}", status_code=status.HTTP_201_CREATED, response_model=schemas.Altname)
def add_altname(brand_name: str, alt_name: str, db:Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    brand = db.query(models.Brand).filter(models.Brand.name == brand_name).first()
    
    if brand == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand with name: {brand_name} does not exist")
    if brand.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    altname_obj = models.Altname(altname=alt_name, brand_id=brand.id)
    db.add(altname_obj)
    db.commit()
    return altname_obj
    
        
# remove alt name
@router.delete("/{brand_name}/{alt_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_altname(brand_name: str,alt_name: str, db:Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):

    brand = db.query(models.Brand).filter(models.Brand.name == brand_name).first()
    
    if brand == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand with name: {brand_name} does not exist")
    if brand.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        
    
    altname_query = db.query(models.Altname).filter(models.Altname.brand_id == brand.id, models.Altname.altname == alt_name)
    altname = altname_query.first()
    if altname == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Alternative name with name: {altname} does not exist")
        
    altname_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# sentiment analysis part